#!/bin/bash

# ==========================================================
# FlexNGIA Congestion Control Manager
# ==========================================================
#
# Commands:
#
#   ./cc.sh
#       Show current active congestion control
#
#   ./cc.sh -l
#       List congestion control modules
#
#   ./cc.sh -s <cc>
#       Load congestion control module
#
#   ./cc.sh -a <cc>
#       Activate congestion control
#
#   ./cc.sh -u <cc>
#       Unload LLM congestion control module (rmmod + remove repo files + clean registry)
#
#   ./cc.sh -c
#       Print all loaded LLM CC modules in one space-separated line
#
# ==========================================================


# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

CC_PATH="/sys/module/tcp_proxy/parameters/delegate_cc"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TRACES_DIR="$SCRIPT_DIR/agent/traces"
REPO_DIR="$TRACES_DIR/repo"
LOADED_FILE="$TRACES_DIR/.loaded_cc"

mkdir -p "$REPO_DIR"

[ -f "$LOADED_FILE" ] || touch "$LOADED_FILE"


# ----------------------------------------------------------
# Load mapping file
# ----------------------------------------------------------

load_mapping() {

    declare -gA MAP_OLD_NEW
    declare -gA MAP_NEW_OLD

    while read -r old new; do
        [ -z "$old" ] && continue
        MAP_OLD_NEW["$old"]="$new"
        MAP_NEW_OLD["$new"]="$old"
    done < "$LOADED_FILE"

}


# ----------------------------------------------------------
# Show active CC
# ----------------------------------------------------------

show_current_cc() {

    if [ -f "$CC_PATH" ]; then
        current_cc=$(tr -d '[:space:]' < "$CC_PATH")
        if [ -z "$current_cc" ]; then
            echo "No congestion control is currently active."
        else
            echo "Current active congestion control: $current_cc"
        fi
    else
        echo "Error: delegate_cc parameter not found."
        exit 1
    fi
}


# ----------------------------------------------------------
# Print all CC modules in one space-separated line:
# union of repo/*.ko names and sysctl list, deduplicated, proxy excluded.
# ----------------------------------------------------------

get_loaded_llm_cc() {

    declare -A seen
    result=()

    # Add all .ko names from repo/
    for ko in "$REPO_DIR"/*.ko; do
        [ -e "$ko" ] || continue
        name=$(basename "$ko" .ko)
        [[ "$name" == "proxy" ]] && continue
        if [[ -z "${seen[$name]}" ]]; then
            seen["$name"]=1
            result+=("$name")
        fi
    done

    # Add sysctl entries not already in the list
    available_cc=$(sysctl -n net.ipv4.tcp_available_congestion_control)
    read -ra kernel_cc <<< "$available_cc"

    for k in "${kernel_cc[@]}"; do
        [[ "$k" == "proxy" ]] && continue
        if [[ -z "${seen[$k]}" ]]; then
            seen["$k"]=1
            result+=("$k")
        fi
    done

    echo "${result[*]}"
}


# ----------------------------------------------------------
# List congestion controls
# ----------------------------------------------------------

list_cc() {

    load_mapping

    active_cc=$(tr -d '[:space:]' < "$CC_PATH" 2>/dev/null)

    available_cc=$(sysctl -n net.ipv4.tcp_available_congestion_control)
    read -ra kernel_cc <<< "$available_cc"

    declare -A LLM_MODULES

    echo ""
    echo "=============================="
    echo "        LLM-Based CC"
    echo "=============================="

    printf "%-20s | %-20s | %-7s | %-12s | %-6s\n" \
        "CC name" "old name" "loaded" "description" "active"

    printf "%-20s-+-%-20s-+-%-7s-+-%-12s-+-%-6s\n" \
        "--------------------" "--------------------" "-------" "-----------" "------"

    for ko in "$REPO_DIR"/*.ko; do

        [ -e "$ko" ] || continue

        new=$(basename "$ko" .ko)

        old="${MAP_NEW_OLD[$new]}"
        [ -z "$old" ] && old="-"

        LLM_MODULES["$new"]=1
        [ "$old" != "-" ] && LLM_MODULES["$old"]=1

        loaded="no"
        for k in "${kernel_cc[@]}"; do
            if [ "$k" == "$new" ]; then
                loaded="yes"
                break
            fi
        done

        marker=""
        [ "$new" == "$active_cc" ] && marker="*"

        printf "%-20s | %-20s | %-7s | %-12s | %-6s\n" \
            "$new" "$old" "$loaded" "-" "$marker"

    done

    while IFS= read -r f; do

        name=$(basename "$f" .c)

        [[ "$name" == *.mod ]] && continue
        [[ -n "${MAP_OLD_NEW[$name]}" ]] && continue
        [ -e "$REPO_DIR/$name.ko" ] && continue

        printf "%-20s | %-20s | %-7s | %-12s | %-6s\n" \
            "$name" "-" "no" "-" ""

    done < <(find "$TRACES_DIR" \
                  -not -path "$REPO_DIR/*" \
                  -type f \
                  -name "*.c" \
                  ! -name "*.mod.c" \
                  2>/dev/null)

    echo ""
    echo "=============================="
    echo "      Linux Built-in CC"
    echo "=============================="

    printf "%-20s | %-20s | %-7s | %-12s | %-6s\n" \
        "CC name" "old name" "loaded" "description" "active"

    printf "%-20s-+-%-20s-+-%-7s-+-%-12s-+-%-6s\n" \
        "--------------------" "--------------------" "-------" "-----------" "------"

    for cc in "${kernel_cc[@]}"; do

        [[ "$cc" == "proxy" ]] && continue

        if [[ -n "${LLM_MODULES[$cc]}" ]]; then
            continue
        fi

        marker=""
        [ "$cc" == "$active_cc" ] && marker="*"

        printf "%-20s | %-20s | %-7s | %-12s | %-6s\n" \
            "$cc" "-" "yes" "-" "$marker"

    done
}


# ----------------------------------------------------------
# Load congestion control module
# ----------------------------------------------------------

load_cc() {

    CC_NAME="$1"

    if [ -z "$CC_NAME" ]; then
        echo "Error: No CC name provided."
        exit 1
    fi

    AVAILABLE=$(sysctl -n net.ipv4.tcp_available_congestion_control)

    if echo "$AVAILABLE" | grep -qw "$CC_NAME"; then
        echo "Module $CC_NAME already loaded."
        return
    fi

    if [ -f "$REPO_DIR/$CC_NAME.ko" ]; then

        echo "Loading promoted module..."

        sudo insmod "$REPO_DIR/$CC_NAME.ko"

        return
    fi

    SRC=$(find "$TRACES_DIR" \
               -not -path "$REPO_DIR/*" \
               -type f \
               -name "$CC_NAME.c" \
               | head -n1)

    if [ -z "$SRC" ]; then
        echo "Error: $CC_NAME.c not found."
        exit 1
    fi

    echo "Promoting module..."

    ORIG_DIR="$(pwd)"

    cp "$SRC" "$REPO_DIR/"

    cd "$REPO_DIR" || exit 1

    OLD_NAME="$CC_NAME"
    NEW_NAME="$CC_NAME"

    echo "Rename module before compilation? [y/N]"
    read -r ans

    if [[ "$ans" == "y" || "$ans" == "Y" ]]; then

        echo "Enter new name:"
        read -r NEW_NAME

        sed -i "s/$OLD_NAME/$NEW_NAME/g" "$OLD_NAME.c"

        mv "$OLD_NAME.c" "$NEW_NAME.c"

        echo "$OLD_NAME $NEW_NAME" >> "$LOADED_FILE"

    fi

    CC_NAME="$NEW_NAME"

cat > Makefile <<EOF
obj-m += ${CC_NAME}.o

all:
	make -C /lib/modules/\$(shell uname -r)/build M=\$(CURDIR) modules

clean:
	make -C /lib/modules/\$(shell uname -r)/build M=\$(CURDIR) clean
EOF

    echo "Compiling module..."

    make clean > /dev/null 2>&1
    make > /dev/null 2>&1

    if [ ! -f "$CC_NAME.ko" ]; then
        echo "Compilation failed."
        cd "$ORIG_DIR" || true
        exit 1
    fi

    echo "Loading module..."

    sudo insmod "$CC_NAME.ko"

    echo "Module loaded: $CC_NAME"

    cd "$ORIG_DIR" || true
}


# ----------------------------------------------------------
# Activate congestion control
# ----------------------------------------------------------

activate_cc() {

    CC_NAME="$1"

    if [ -z "$CC_NAME" ]; then
        echo "Error: No CC name provided."
        exit 1
    fi

    AVAILABLE=$(sysctl -n net.ipv4.tcp_available_congestion_control)

    if ! echo "$AVAILABLE" | grep -qw "$CC_NAME"; then

        if [ -f "$REPO_DIR/$CC_NAME.ko" ]; then

            echo "Module not loaded (reboot?). Auto-loading from repo..."

            sudo insmod "$REPO_DIR/$CC_NAME.ko"

            AVAILABLE=$(sysctl -n net.ipv4.tcp_available_congestion_control)

            if ! echo "$AVAILABLE" | grep -qw "$CC_NAME"; then
                echo "Error: insmod succeeded but $CC_NAME still not visible in kernel."
                exit 1
            fi

            echo "Module loaded: $CC_NAME"

        else

            echo "Error: $CC_NAME not loaded and no compiled .ko found in repo."
            echo "Use:"
            echo "  sudo ./cc.sh -s $CC_NAME"
            exit 1

        fi

    fi

    echo "$CC_NAME" | sudo tee "$CC_PATH" > /dev/null

    echo "Activated congestion control: $CC_NAME"
}


# ----------------------------------------------------------
# Unload LLM congestion control module
# ----------------------------------------------------------

unload_cc() {

    CC_NAME="$1"

    if [ -z "$CC_NAME" ]; then
        echo "Error: No CC name provided."
        exit 1
    fi

    load_mapping

    is_llm=0
    [ -f "$REPO_DIR/$CC_NAME.ko" ]    && is_llm=1
    [ -n "${MAP_NEW_OLD[$CC_NAME]}" ]  && is_llm=1
    [ -n "${MAP_OLD_NEW[$CC_NAME]}" ]  && is_llm=1

    if [ "$is_llm" -eq 0 ]; then
        echo "Error: '$CC_NAME' is not an LLM-managed module. Only LLM CC modules can be unloaded with this command."
        exit 1
    fi

    active_cc=$(tr -d '[:space:]' < "$CC_PATH" 2>/dev/null)

    if [ "$CC_NAME" == "$active_cc" ]; then
        echo "Error: '$CC_NAME' is currently active. Switch to another congestion control before unloading."
        echo "Use:"
        echo "  sudo ./cc.sh -a <other_cc>"
        exit 1
    fi

    AVAILABLE=$(sysctl -n net.ipv4.tcp_available_congestion_control)

    if echo "$AVAILABLE" | grep -qw "$CC_NAME"; then

        echo "Unloading kernel module: $CC_NAME"

        sudo rmmod "$CC_NAME"

        if [ $? -ne 0 ]; then
            echo "Error: rmmod failed for '$CC_NAME'. The module may be in use."
            exit 1
        fi

        echo "Kernel module removed."

    else
        echo "Module '$CC_NAME' is not currently loaded in kernel (skipping rmmod)."
    fi

    echo "Removing repo files for '$CC_NAME'..."

    shopt -s nullglob

    repo_files=( "$REPO_DIR/$CC_NAME"* "$REPO_DIR/.$CC_NAME"* )

    if [ ${#repo_files[@]} -eq 0 ]; then
        echo "No repo files found for '$CC_NAME'."
    else
        for f in "${repo_files[@]}"; do
            echo "  Removing: $f"
            rm -f "$f"
        done
    fi

    shopt -u nullglob

    if grep -qw "$CC_NAME" "$LOADED_FILE" 2>/dev/null; then

        echo "Removing registry entry for '$CC_NAME' from .loaded_cc..."

        TMPFILE=$(mktemp)

        while read -r old new; do
            [ -z "$old" ] && continue
            if [ "$old" == "$CC_NAME" ] || [ "$new" == "$CC_NAME" ]; then
                echo "  Removed entry: $old $new"
            else
                echo "$old $new" >> "$TMPFILE"
            fi
        done < "$LOADED_FILE"

        cp "$TMPFILE" "$LOADED_FILE"
        rm -f "$TMPFILE"

    else
        echo "No registry entry found for '$CC_NAME' in .loaded_cc."
    fi

    echo "Done. '$CC_NAME' has been fully unloaded and removed."
}


# ----------------------------------------------------------
# Dispatcher
# ----------------------------------------------------------

case "$1" in

    -ls)
        list_cc
        ;;

    -s)
        load_cc "$2"
        ;;

    -a)
        activate_cc "$2"
        ;;

    -u)
        unload_cc "$2"
        ;;

    -l)
        get_loaded_llm_cc
        ;;

    *)
        show_current_cc
        ;;

esac


tar --exclude='./agent/venv' --exclude='./backup' -czvf cc-agent-$(date +%Y%m%d-%H%M).tar.gz .
mv *.tar.gz backup/ 
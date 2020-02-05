# tshark is required
if ! [ -x "$(command -v tshark)" ]; then
  echo 'Error: tshark is not installed.' >&2
  else echo 'tshark is installed' >&2
fi

# python3 is required
if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: python3 is not installed.' >&2
  else echo 'python3 is installed' >&2
fi

# zeek is required
if ! [ -x "$(command -v zeek)" ]; then
  echo 'Error: zeek is not installed.' >&2
  else echo 'zeek is installed' >&2
fi

# there should be local pcapspliiterr binary
if ! [ -x "$(command -v ./PcapSplitter)" ]; then
  echo 'Error: PcapSplitter not found.' >&2
  else echo 'PcapSplitter available' >&2
fi

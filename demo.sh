cd data/wikipedia_sci
if [ ! -e text8 ]; then
  cd ../../
  wget http://mattmahoney.net/dc/text8.zip -O text8.gz
  mv text8.gz data/wikipedia_sci && cd data/wikipedia_sci
  gzip -d text8.gz -f
  cd ../../
fi




if [ ! -e glove.6B.* ]; then
	wget http://nlp.stanford.edu/data/glove.6B.zip -O glove.6B.zip
	unzip glove.6B.zip
	rm glove.6B.zip
fi


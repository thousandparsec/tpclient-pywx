#! /bin/sh

for xrc in *.xrc; do
	python generate.py $xrc
done

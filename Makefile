build:
	docker build ./ -t stargaze:latest


build-dev:
	docker build ./dev/ -t stargaze-ui:latest

run-dev:
	docker run -v `pwd`:/app -it --privileged --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" stargaze-ui
# Jing

A prototype of performing instruments in a simple AR environment.

This project was developed during [Sotoon](https://sotoon.ir) Hackathon 1399 and won the best idea award.

## Demo

What these videos

- [Playing with Piano](https://sesajad.me/box/projects/jing/Piano.mp4)
- [Playing with Drums](https://sesajad.me/box/projects/jing/Drums.mp4)
- [Playing with Salar<sup>*</sup>](https://sesajad.me/box/projects/jing/Salar.mp4)

<sup>*</sup>: Salar is a string instrument designed by MohammadAmin Salarkia.



## Setup

This project is written by python3 and it's tested along versions 3.7 to 3.9.

1. Install synthfluid.
2. I'ts recommended to use a venv.
3. Install requirements
```
pip install -r requirements.txt
```
4. Choose your instruments and fix other parameters in `src/config.py`
5. Run!
```
python src/main.py
```

## TODO

- [ ] create a webapp
- [ ] improve gesture detection
- [ ] add more and more instruments.
- [ ] a real (stereoscopic) VR experience

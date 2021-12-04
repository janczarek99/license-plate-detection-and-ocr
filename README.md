# License plate detection and OCR

## Cel projektu

Celem projektu było stworzenie serwisu do rozpoznawania tablic rejestracyjnych na podstawie filmu (format mp4, długość do 15 sekund) do zastosowania w automatyzacji otwierania bram garażowych, czy monitorowania ruchu w pobliżu osiedla.

## Skład zespołu

* Michał Gajda - [github](https://github.com/michauga)
* Damian Janczarek - [github](https://github.com/janczarek99)
* Hubert Piłka - [github](https://github.com/MrBallOG)
* Tomasz Stańczuk - [github](https://github.com/TommyV2)

## Stos technologiczny

* React
* Python (FastAPI)
* Docker
* Azure Custom Vision (Object Detection)
* Azure Computer Vision (OCR)
* Azure Container Services:
  * Container Instances
  * Container Registry
* Azure App Service

## Diagram architektury

![architektura](resources/architecture/architecture.svg)

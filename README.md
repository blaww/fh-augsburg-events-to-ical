# FH Augsburg Events to iCal

[![](https://images.microbadger.com/badges/version/svenfritsch/fh-augsburg-events-to-ical.svg)](https://microbadger.com/images/svenfritsch/fh-augsburg-events-to-ical "Get your own version badge on microbadger.com")

This project was created to showecase howmuch simpler it is to distribute your code dockerized. 
Even if it's just a simple python script.

## Dependencies

- [Docker](https://www.docker.com/)

## Usage

```bash
docker run -v $(pwd):/app/out/ svenfritsch/fh-augsburg-events-to-ical:latest
```

## Development

### Build Project

```bash
docker build -t svenfritsch/fh-augsburg-events-to-ical .
```

### Run Project

```bash
docker run -v $(pwd):/app/out/ svenfritsch/fh-augsburg-events-to-ical
```
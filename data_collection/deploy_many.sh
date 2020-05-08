for i in $(seq 45 53);
do
    python deploy.py gs://animalese-to-text/videos/switch-playthroughs-playlist/$i gs://animalese-to-text/videos/switch-playthroughs-playlist-blathers/
done
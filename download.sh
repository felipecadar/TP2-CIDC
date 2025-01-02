ds1='https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_ds1.csv'
ds2='https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_ds2.csv'
songs='https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_songs.csv'

DST='datasets'
flags='--no-check-certificate'

mkdir -p $DST
wget -O $DST/2023_spotify_ds1.csv $ds1 $flags
wget -O $DST/2023_spotify_ds2.csv $ds2 $flags
wget -O $DST/2023_spotify_songs.csv $songs $flags

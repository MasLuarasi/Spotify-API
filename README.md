# Spotify-API
Seeing how an album's prereleased tracks fare in comparison with the rest of the album in terms of streams
Using the Spotify API via RapidAPI, this code will get the discography for a list of artists.
This artist name, id, album name, id will be written to a csv file 'artistAlbum.csv'.
After geting the discography info, the next step will read the data from the initial csv to get the track list and streams for each song in the album.
The artist name, album name, track name, and streams will be written to a second csv 'albumTrack.csv. 
I manually removed a few lines of unnecessary data. for both csv files. 
In addition, for the second csv 'albumTrack.csv', I added another column of data indicating whether or not this track was prereleased or not. I added this info manually as some of the data is missing on spotify.

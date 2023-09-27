import requests
import csv
import pandas as pd
import os

def getArtistID(artistName):#STEP 1: Search the artist to get their ID
  url = 'https://spotify23.p.rapidapi.com/search/'
  querystring = {'q': artistName, 'type': 'artists', 'limit': '1'}
  headers = {
    'X-RapidAPI-Key': '4125e08ab5msh1e35e54946ee894p1de70djsn0b70aa45221f',
    'X-RapidAPI-Host': 'spotify23.p.rapidapi.com'
  }
  response = requests.get(url, headers=headers, params=querystring).json()#Get the response and change it to json format
  artistData = response['artists']['items'][0]['data']#Pull out the section with the artist information
  artistName = artistData['profile']['name']#Extract the name
  artistID = artistData['uri'][15:]#Extract the ID
  print('\n' + artistName)#Keep track while program runs. If there is an issue, see which artist caused it
  getOverview(artistName, artistID)#Execute step 2

def getAlbumEP(data, type, artistName, artistID):#Get the album/EP information
  discographyData = data[type]['items']#After getting past the type, 'Albums' or 'Singles' (These are where EPs are listed), the format in the response is the same
  for item in discographyData:#For each item listed here
    info = item['releases']['items'][0]
    if(info['type'] == 'EP' or info['type'] == 'ALBUM'):#If it is one of the two we are looking for
      albumName = info['name']#Extract the name
      albumID = info['id']#Extract the ID
      rowData = [artistName, artistID, albumName, albumID]
      artistAlbumData.append(rowData)#Keep track of all the data here, then write it after we have all of it
      print('\n', albumName)

def getOverview(artistName, artistID):#STEP 2: Using the artist ID that we can find from step 1, get an overview of the artist
  url = 'https://spotify23.p.rapidapi.com/artist_overview/'
  querystring = {'id': artistID}
  headers = {
    'X-RapidAPI-Key': '4125e08ab5msh1e35e54946ee894p1de70djsn0b70aa45221f',
    'X-RapidAPI-Host': 'spotify23.p.rapidapi.com'
  }
  response = requests.get(url, headers=headers, params=querystring).json()
  albumData = response['data']['artist']['discography']
  #In the response we get from the API, Albums and EPs are labeled differently. Have to put it into an try except incase an author has one but not the other
  try:
    getAlbumEP(albumData, 'albums', artistName, artistID)
  except:
    pass
  try:
        getAlbumEP(albumData, 'singles', artistName, artistID)
  except:
     pass
  with open('artistAlbum.csv', mode='w', newline='') as f:#Write the data containing the artist and album info to the csv 
    writer = csv.writer(f)
    writer.writerow(['Artist', 'Artist ID', 'Album', 'Album ID'])
    writer.writerows(artistAlbumData)
  f.close()

def getTrackList(artistName, albumName, albumID):#STEP 3: Get the album track list with the album id from previous step
  url = 'https://spotify23.p.rapidapi.com/album_tracks/'
  querystring = {'id': albumID, 'offset': '0', 'limit': '300'}
  headers = {
    'X-RapidAPI-Key': '4125e08ab5msh1e35e54946ee894p1de70djsn0b70aa45221f',
    'X-RapidAPI-Host': 'spotify23.p.rapidapi.com'
  }
  response = requests.get(url, headers=headers, params=querystring).json()
  trackData = response['data']['album']['tracks']['items']
  for song in trackData:#For every song in the album
    info = song['track']
    trackName = info['name']#Extract the name
    trackPlayCount = info['playcount']#Extract how many streams it has
    rowData = [artistName, albumName, trackName, trackPlayCount]
    albumTrackData.append(rowData)#Keep track of data before writing it to csv at end
  with open('albumTrack.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Artist', 'Album', 'Track', 'Plays'])
    writer.writerows(albumTrackData)
  f.close()

#------------------------------------------------------------------------------------------------------------------------------------
artistList = ['Arctic Monkeys', 'Ashe', 'Backseat Lovers', 'Beach Bunny', 'Between Friends',
              'Billie Eilish', 'Breakup Shoes', 'Briston Maroney', 'Cage The Elephant',
              'Claire Rosinkranz', 'Clairo', 'Coin', 'Conan Gray', 'Dayglow', 'Del Water Gap',
              'Doja Cat', 'Dreamers', 'Faze Wave', 'girl in red', 'Glass Animals', 'Jeremy Zucker',
              'Lexi Jayde', 'Lovely The Band', 'mxmtoon', 'New Politics', 'Olivia Rodrigo',
              'Perfume Genius', 'Peter McPoland', 'Phoebe Bridgers', 'Phoneboy', 'Saint Motel',
              'San Cisco', 'Smallpools', 'Soccer Mommy', 'The Academic', 'The Regrettes',
              'The Wrecks', 'Vistas', 'Wallows']#List of artists to look at. Indie/Alt artists usually prerelease songs prior to a 
                                                #full album release. Major pop stars less so, they also have so much data because of 
                                                #how much they release, and given our limited API calls, they are not being considered
artistAlbumData = []#Keep track of ['Artist', 'Artist ID', 'Album', 'Album ID']
albumTrackData = []#Keep track of ['Artist', 'Album', 'Track', 'Plays']

# for artist in artistList:
#    getArtistID(artist)#Getting the artist info and discography for each one in the list

# with open('artistAlbum.csv', mode='r', newline='') as f:#Reading and getting the track list for every album that we recorded in step 1
#   reader = csv.reader(f)
#   next(reader)#Ignore the header row
#   for line in reader:
#     getTrackList(line[0], line[2], line[3])
# f.close()

df = pd.read_csv('albumTrack.csv')#Using pandas to read the csv into a dataframe
totalStreams = df.groupby(['Artist', 'Album'])['Plays'].transform('sum')#Sum up the streams for songs in each album. EX: Album a has songs b(5 streams), c(10 streams), and d(15 streams). Album a's songs have a total of 30 streams
df['Percentage'] = round(df['Plays'] / totalStreams * 100, 2)#Getting the percentage share of streams for each song. EX: Referencing example above. song c represents 33.33% of Album a's total streams
os.remove('albumTrack.csv')#Remove the original file
df.to_csv('albumTrack.csv', index=False)#Replace it with the new data

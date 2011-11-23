import json
from django.contrib.auth.models import User
from udj.tests.testcases import User1TestCase
from udj.tests.testcases import User2TestCase
from udj.tests.testcases import User3TestCase
from udj.models import Event
from udj.models import LibraryEntry
from udj.models import EventGoer
from udj.models import FinishedEvent
from udj.models import AvailableSong
from decimal import Decimal

class GetEventsTest(User1TestCase):
  def testGetEvents(self):
    response = self.doGet('/udj/events/48.2222/-88.44454')
    self.assertEqual(response.status_code, 200)
    events = json.loads(response.content)
    self.assertEqual(events[0]['id'], 1) 
    self.assertEqual(events[0]['name'], 'First Party') 
    self.assertEqual(events[0]['latitude'], 40.113523) 
    self.assertEqual(events[0]['longitude'], -88.224006) 
    self.assertTrue("password" not in events[0])
    self.assertTrue("password_hash" not in events[0])

class CreateEventTest(User1TestCase):
  def testCreateEvent(self):
    partyName = "A Bitchn' Party"
    event = {'name' : partyName } 
    response = self.doJSONPut('/udj/events/event', json.dumps(event))
    self.assertEqual(response.status_code, 201, "Error: " + response.content)
    self.assertEqual(json.loads(response.content)['event_id'] ,2)
    addedEvent = Event.objects.filter(id=2)
    self.assertEqual(addedEvent[0].name, partyName)

class EndEventTest(User1TestCase):
  def testEndEvent(self):
    response = self.doDelete('/udj/events/1')
    self.assertEqual(len(Event.objects.filter(id=1)), 0)
    finishedEvent = FinishedEvent.objects.filter(party_id=1)
    self.assertEqual(len(finishedEvent), 1)
    finishedEvent = finishedEvent[0]
    self.assertEqual(finishedEvent.name, 'First Party') 
    self.assertEqual(finishedEvent.latitude, Decimal('40.113523'))
    self.assertEqual(finishedEvent.longitude, Decimal('-88.224006'))
    self.assertEqual(finishedEvent.host, User.objects.filter(id=2)[0])

class JoinEventTest(User3TestCase):
  def testJoinEvent(self):
    response = self.doPut('/udj/events/1/user')
    self.assertEqual(response.status_code, 201)
    event_goer_entries = EventGoer.objects.filter(event__id=1, user__id=3)
    self.assertEqual(len(event_goer_entries),1) 
    
class LeaveEventTest(User2TestCase):
  def testLeaveEvent(self):
    response = self.doDelete('/udj/events/1/3')
    self.assertEqual(response.status_code, 200, response.content)
    event_goer_entries = EventGoer.objects.filter(event__id=1, user__id=3)
    self.assertEqual(len(event_goer_entries), 0)

class KickUserTest(User1TestCase):
  def testKickUser(self):
    response = self.doDelete('/udj/events/1/3')
    self.assertEqual(response.status_code, 200, response.content)
    event_goer_entries = EventGoer.objects.filter(event__id=1, user__id=3)
    self.assertEqual(len(event_goer_entries), 0)

#TODO still need to test the max_results parameter
class TestGetAvailableMusic(User2TestCase):
  def verifyExpectedResults(self, results, realSongs):
   realIds = [song.host_lib_song_id for song in realSongs]
   for song in results:
     self.assertTrue(song['id'] in realIds)
 
  def testGetAlbum(self): 
   response = self.doGet('/udj/events/1/available_music?query=blue')
   self.assertEqual(response.status_code, 200, response.content)
   results = json.loads(response.content)
   self.assertEqual(len(results), 2)
   realSongs = LibraryEntry.objects.filter(album="Blue")
   self.verifyExpectedResults(results, realSongs)

  def testGetArtist(self): 
   response = self.doGet(
    '/udj/events/1/available_music?query=smashing+pumpkins')
   self.assertEqual(response.status_code, 200, response.content)
   results = json.loads(response.content)
   self.assertEqual(len(results), 1)
   realSongs = LibraryEntry.objects.filter(artist="The Smashing Pumpkins")
   self.verifyExpectedResults(results, realSongs)

  def testGetSong(self):
   response = self.doGet(
    '/udj/events/1/available_music?query=Never+Let+You+Go')
   self.assertEqual(response.status_code, 200, response.content)
   results = json.loads(response.content)
   self.assertEqual(len(results), 1)
   realSongs = LibraryEntry.objects.filter(song="Never Let You Go")
   self.verifyExpectedResults(results, realSongs)

  def testSongNotAvailable(self): 
   response = self.doGet(
    '/udj/events/1/available_music?query=rage+against+the+machine')
   self.assertEqual(response.status_code, 200, response.content)
   results = json.loads(response.content)
   self.assertEqual(len(results), 0)

class TestPutAvailableMusic(User1TestCase):
  def testPut(self): 
   toAdd=[13]
   response = self.doJSONPut('/udj/events/1/available_music', json.dumps(toAdd))
   self.assertEqual(response.status_code, 201, response.content)
   results = json.loads(response.content)
   self.assertEqual(len(results), 1)
   self.assertEqual(results[0], 13)
   addedSong = AvailableSong.objects.filter(
    library_entry__host_lib_song_id=13, library_entry__owning_user__id=2)
   self.assertEqual(len(addedSong), 1)

class TestCantPutMusic(User2TestCase):
  def testPut(self): 
   toAdd=[13]
   response = self.doJSONPut('/udj/events/1/available_music', json.dumps(toAdd))
   self.assertEqual(response.status_code, 403, response.content)

#Added Fuxes
import unittest
import os
from urllib import response
os.environ['TESTING']='true'

from app import app
from app import TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp (self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "content=\"Personal Portfolio\"" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello, I am John')
        assert first_post.id == 1
    
    def test_malformed_timeline (self):
        response = self.client.post('/api/timeline_post', data={"email":"john@email.com", "content":"Hello"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Name" in html
        response = self.client.post('/api/timeline_post', data={"name":"john@email.com", "content":"Hello"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Email" in html
        response = self.client.post('/api/timeline_post', data={"name":"l+Ratio", "email":"john.com", "content":"Hello"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Email" in html
        response = self.client.post('/api/timeline_post', data={"name":"Joe", "email":"john@email.com"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Content" in html
        response = self.client.post('/api/timeline_post', data={"name":"Joe", "email":"john@email.com", "content":""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Content" in html
        response = self.client.get('/api/timeline_post')
        json = response.get_json()
        assert len(json["timeline_posts"]) == 0
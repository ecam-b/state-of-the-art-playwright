from typing import Dict, Any
from apis.base_api import BaseAPI


class PostAPI(BaseAPI):
    """
    API client for post management using JSONPlaceholder.
    This is a generic example API for the starter kit.
    """
    
    def __init__(self, request_context: Any):
        super().__init__(request_context)
        self.base_url = "https://jsonplaceholder.typicode.com"
    
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """
        Get post by ID.
        Returns post data as dictionary.
        """
        self.logger.debug(f"Getting post: {post_id}")
        
        response = self.request.get(f"{self.base_url}/posts/{post_id}")
        
        self._log_request("GET", f"/posts/{post_id}", response.status)
        
        if response.status != 200:
            self.logger.error(f"Failed to get post: {response.text()}")
            assert False, f"Error getting post: {response.text()}"
        
        post_data = response.json()
        self.logger.info(f"Post retrieved successfully (ID: {post_id})")
        
        return post_data
    
    def get_posts(self, user_id: int = None) -> list[Dict[str, Any]]:
        """
        Get list of posts, optionally filtered by user ID.
        Returns list of posts.
        """
        url = f"{self.base_url}/posts"
        if user_id:
            url += f"?userId={user_id}"
            self.logger.debug(f"Getting posts for user: {user_id}")
        else:
            self.logger.debug("Getting all posts")
        
        response = self.request.get(url)
        
        self._log_request("GET", f"/posts", response.status)
        
        if response.status != 200:
            self.logger.error(f"Failed to get posts: {response.text()}")
            assert False, f"Error getting posts: {response.text()}"
        
        posts_data = response.json()
        self.logger.info(f"Retrieved {len(posts_data)} posts")
        
        return posts_data
    
    def create_post(self, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """
        Create new post.
        Returns created post data as dictionary.
        """
        self.logger.debug(f"Creating post: {title}")
        
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        
        response = self.request.post(
            f"{self.base_url}/posts",
            data=payload
        )
        
        self._log_request("POST", "/posts", response.status)
        
        if response.status != 201:
            self.logger.error(f"Failed to create post: {response.text()}")
            assert False, f"Error creating post: {response.text()}"
        
        post_data = response.json()
        self.logger.info(f"Post created: {title} (ID: {post_data.get('id')})")
        
        return post_data
    
    def update_post(self, post_id: int, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """
        Update post by ID.
        Returns updated post data as dictionary.
        """
        self.logger.debug(f"Updating post: {post_id}")
        
        payload = {
            "id": post_id,
            "title": title,
            "body": body,
            "userId": user_id
        }
        
        response = self.request.put(
            f"{self.base_url}/posts/{post_id}",
            data=payload
        )
        
        self._log_request("PUT", f"/posts/{post_id}", response.status)
        
        if response.status != 200:
            self.logger.error(f"Failed to update post: {response.text()}")
            assert False, f"Error updating post: {response.text()}"
        
        post_data = response.json()
        self.logger.info(f"Post updated: {title} (ID: {post_id})")
        
        return post_data
    
    def delete_post(self, post_id: int) -> None:
        """Delete post by ID."""
        self.logger.debug(f"Deleting post: {post_id}")
        
        response = self.request.delete(f"{self.base_url}/posts/{post_id}")
        
        self._log_request("DELETE", f"/posts/{post_id}", response.status)
        
        if response.status != 200:
            self.logger.error(f"Failed to delete post {post_id}: {response.text()}")
            assert False, f"Error deleting post: {response.text()}"
        
        self.logger.info(f"Post deleted: {post_id}")
    
    # Override login as JSONPlaceholder doesn't require authentication
    def login(self, username: str = "", password: str = "", response_user: str = "true") -> str:
        """
        JSONPlaceholder doesn't require authentication.
        This override prevents authentication errors.
        """
        self.logger.info("JSONPlaceholder API doesn't require authentication")
        self.token = "no-auth-required"
        return self.token
    
    def _get_headers(self) -> Dict[str, str]:
        """
        JSONPlaceholder doesn't require auth headers.
        Returns empty dict.
        """
        return {}

import pytest
from pydantic import ValidationError
from apis.schemas.post_schemas import PostResponse, PostCreateResponse
from utils.data_provider import DataProvider


def test_get_single_post(api_client):
    """
    Validate single post retrieval with Pydantic schema.
    Tests GET operation and response structure validation.
    """
    # Arrange
    # - Get test data from JSON.
    post_data_config = DataProvider.get_data("posts", "get_single_post")
    POST_ID = post_data_config["post_id"]
    EXPECTED_USER_ID = post_data_config["expected_user_id"]
    
    # Act
    # - Get post data via API.
    post_data = api_client.posts.get_post(POST_ID)
    
    # Assert
    # - Validate response structure with Pydantic schema.
    try:
        validated_post = PostResponse(**post_data)
        
        # - Validate post ID matches request.
        assert validated_post.id == POST_ID, "Post ID should match requested ID"
        # - Validate user ID is correct.
        assert validated_post.userId == EXPECTED_USER_ID, "User ID should match expected value"
        # - Validate title is not empty.
        assert len(validated_post.title) > 0, "Title should not be empty"
        # - Validate body is not empty.
        assert len(validated_post.body) > 0, "Body should not be empty"
        
    except ValidationError as e:
        pytest.fail(f"API response schema validation failed: {e}")


def test_get_user_posts(api_client):
    """
    Validate retrieval of posts filtered by user.
    Tests query parameter filtering functionality.
    """
    # Arrange
    # - Get test data from JSON.
    user_posts_data = DataProvider.get_data("posts", "get_user_posts")
    USER_ID = user_posts_data["user_id"]
    EXPECTED_MIN_POSTS = user_posts_data["expected_min_posts"]
    
    # Act
    # - Get posts for specific user via API.
    posts_data = api_client.posts.get_posts(user_id=USER_ID)
    
    # Assert
    # - Validate at least one post is returned.
    assert len(posts_data) >= EXPECTED_MIN_POSTS, f"Should return at least {EXPECTED_MIN_POSTS} post(s)"
    
    # - Validate first post structure with Pydantic.
    try:
        first_post = PostResponse(**posts_data[0])
        
        # - Validate all posts belong to requested user.
        assert first_post.userId == USER_ID, "Post should belong to requested user"
        
    except ValidationError as e:
        pytest.fail(f"API response schema validation failed: {e}")


def test_create_post(api_client, unique_name):
    """
    Validate post creation with Pydantic schema.
    Tests POST operation and response structure.
    """
    # Arrange
    # - Get test data from JSON.
    create_post_data = DataProvider.get_data("posts", "create_post")
    POST_TITLE = f"{create_post_data['title']} {unique_name}"
    POST_BODY = create_post_data["body"]
    USER_ID = create_post_data["user_id"]
    
    # Act
    # - Create post via API.
    response_data = api_client.posts.create_post(
        title=POST_TITLE,
        body=POST_BODY,
        user_id=USER_ID
    )
    
    # Assert
    # - Validate response structure with Pydantic schema.
    try:
        validated_response = PostCreateResponse(**response_data)
        
        # - Validate title matches request.
        assert validated_response.title == POST_TITLE, "Title should match request"
        # - Validate body matches request.
        assert validated_response.body == POST_BODY, "Body should match request"
        # - Validate user ID matches request.
        assert validated_response.userId == USER_ID, "User ID should match request"
        # - Validate post ID is returned.
        assert validated_response.id is not None, "Should return created post ID"
        
    except ValidationError as e:
        pytest.fail(f"API response schema validation failed: {e}")


def test_update_post(api_client):
    """
    Validate post update operation via PUT request.
    Tests update endpoint and response structure.
    """
    # Arrange
    # - Get test data from JSON.
    update_post_data = DataProvider.get_data("posts", "update_post")
    POST_ID = update_post_data["post_id"]
    UPDATED_TITLE = update_post_data["title"]
    UPDATED_BODY = update_post_data["body"]
    USER_ID = update_post_data["user_id"]
    
    # Act
    # - Update post via API.
    response_data = api_client.posts.update_post(
        post_id=POST_ID,
        title=UPDATED_TITLE,
        body=UPDATED_BODY,
        user_id=USER_ID
    )
    
    # Assert
    # - Validate post ID matches request.
    assert response_data["id"] == POST_ID, "Post ID should match request"
    # - Validate title was updated.
    assert response_data["title"] == UPDATED_TITLE, "Title should be updated"
    # - Validate body was updated.
    assert response_data["body"] == UPDATED_BODY, "Body should be updated"
    # - Validate user ID matches request.
    assert response_data["userId"] == USER_ID, "User ID should match request"


def test_delete_post(api_client):
    """
    Validate post deletion via DELETE request.
    Tests delete endpoint returns success status.
    """
    # Arrange
    # - Get test data from JSON.
    delete_post_data = DataProvider.get_data("posts", "delete_post")
    POST_ID = delete_post_data["post_id"]
    
    # Act & Assert
    # - Delete post via API (should not raise exception).
    api_client.posts.delete_post(POST_ID)
    
    # Note: JSONPlaceholder simulates deletion but doesn't actually remove data.
    # In real scenarios, you would verify the post is actually deleted.

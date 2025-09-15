# import pytest
# from httpx import AsyncClient, ASGITransport
# from app.main import app


# @pytest.mark.anyio
# async def test_categories():
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         login_data = {"username": "testuser", "password": "1234"}
#         login_response = await ac.post("/api/v1/auth/login", data=login_data)
#         token = login_response.json()
#         auth = {"Authorization": f"Bearer {token}"}

#         response = await ac.get("/api/v1/categories", headers=auth)

#     assert response.status_code == 200

#     expected = [
#         {"name": "Salary", "type": "income"},
#         {"name": "Sales", "type": "income"},
#         {"name": "Rent", "type": "expense"},
#         {"name": "Food", "type": "expense"},
#         {"name": "Transport", "type": "expense"},
#         {"name": "Savings", "type": "investment"},
#         {"name": "Cryptocurrency", "type": "investment"},
#         {"name": "Utilities", "type": "expense"},
#         {"name": "Entertainment", "type": "expense"},
#         {"name": "Healthcare", "type": "expense"},
#         {"name": "Education", "type": "expense"},
#         {"name": "Insurance", "type": "expense"},
#         {"name": "Miscellaneous", "type": "expense"},
#     ]

#     assert response.json() == expected

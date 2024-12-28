# from pinecone import Pinecone, ServerlessSpec
# import logging
# from datetime import datetime, timezone

# # Initialize Pinecone with the correct method
# pc = Pinecone(api_key="pcsk_5UuJNF_RSdw4brKcj3HdmF6T35fbqZxpgRqhzi1YXVhZvLvzGnhXPa2zesbWBTQD3NcJcr")

# # Define the index name
# index_name = "quickstart"

# # Check if the index exists, if not, create it
# # Check if the index exists, if not, create it
# if index_name not in pc.list_indexes().names():
#     # Create index with the necessary spec
#     pc.create_index(
#         name=index_name,
#         dimension=1024,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1",
#         )
#     )

# # Initialize the index
# index = pc.Index(index_name)

# # Initialize logger
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def log_activity(activity: str, user_id: str, timestamp: datetime = None):
#     """
#     Log activity to Pinecone by saving it to an index.
#     :param activity: The activity message to log.
#     :param user_id: The ID of the user performing the activity.
#     :param timestamp: The timestamp of the activity. If not provided, current time will be used.
#     """
#     if timestamp is None:
#         timestamp = datetime.utcnow()
#         timestamp = datetime.now(timezone.utc)
    
#     # Format the activity message with timestamp
#     activity_data = {
#         "user_id": user_id,
#         "activity": activity,
#         "timestamp": timestamp.isoformat()
#     }

#     try:
#         # Upsert activity data into Pinecone
#         index.upsert(
#             vectors=[{
#                 'id': user_id,
#                 'values': activity_data,  # The activity data can be your embedding
#                 'metadata': {'timestamp': timestamp.isoformat()}
#             }]
#         )
#         logger.info(f"Activity logged for user {user_id} at {timestamp}")
#     except Exception as e:
#         logger.error(f"Error logging activity: {str(e)}")
#         raise

# # Example usage
# log_activity("User logged in", "user123")

# ============================================================
# Hands-On 5: MongoDB CRUD & Aggregation Pipeline
# File: hands_on_5_mongodb.py
# Location: C:\DigitalNurture5\Module1_DatabaseIntegration\hands_on_5\
# ============================================================

from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime

# --- Connect to MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["college_nosql"]           # Creates database if not exists
feedback = db["feedback"]              # Creates collection if not exists

print("Connected to MongoDB successfully.")

# ============================================================
# TASK 1: Insert Documents
# ============================================================

# Clear collection for fresh start (safe re-run)
feedback.delete_many({})

# Insert 10+ feedback documents
sample_feedback = [
    {
        "student_id":   1,
        "course_code":  "CS101",
        "semester":     "2022-ODD",
        "rating":       5,
        "comments":     "Excellent teaching. Would highly recommend.",
        "tags":         ["challenging", "well-structured", "good-examples"],
        "submitted_at": datetime(2022, 11, 30, 10, 15, 0),
        "attachments":  [{"filename": "notes.pdf", "size_kb": 240}]
    },
    {
        "student_id":   2,
        "course_code":  "CS101",
        "semester":     "2022-ODD",
        "rating":       4,
        "comments":     "Good content but lectures were too fast.",
        "tags":         ["challenging", "fast-paced"],
        "submitted_at": datetime(2022, 12, 1, 14, 30, 0),
        "attachments":  []
    },
    {
        "student_id":   5,
        "course_code":  "CS101",
        "semester":     "2022-ODD",
        "rating":       3,
        "comments":     "Average. Could be better organized.",
        "tags":         ["average", "needs-improvement"],
        "submitted_at": datetime(2022, 12, 2, 9, 0, 0),
        "attachments":  [{"filename": "assignment.pdf", "size_kb": 120}]
    },
    {
        "student_id":   1,
        "course_code":  "CS102",
        "semester":     "2022-ODD",
        "rating":       4,
        "comments":     "Very practical and useful.",
        "tags":         ["practical", "well-structured"],
        "submitted_at": datetime(2022, 11, 28, 11, 0, 0)
        # No attachments field — MongoDB allows this (schema-less)
    },
    {
        "student_id":   5,
        "course_code":  "CS102",
        "semester":     "2022-ODD",
        "rating":       5,
        "comments":     "Best course this semester!",
        "tags":         ["excellent", "well-structured", "good-examples"],
        "submitted_at": datetime(2022, 12, 5, 16, 0, 0),
        "attachments":  []
    },
    {
        "student_id":   3,
        "course_code":  "EC101",
        "semester":     "2021-ODD",
        "rating":       4,
        "comments":     "Solid fundamentals covered.",
        "tags":         ["informative", "challenging"],
        "submitted_at": datetime(2021, 11, 20, 10, 0, 0),
        "attachments":  []
    },
    {
        "student_id":   6,
        "course_code":  "EC101",
        "semester":     "2021-EVEN",
        "rating":       2,
        "comments":     "Too theoretical, not enough examples.",
        "tags":         ["theoretical", "needs-improvement"],
        "submitted_at": datetime(2021, 5, 15, 9, 0, 0),
        "attachments":  []
    },
    {
        "student_id":   4,
        "course_code":  "ME101",
        "semester":     "2023-ODD",
        "rating":       5,
        "comments":     "Phenomenal professor.",
        "tags":         ["excellent", "engaging"],
        "submitted_at": datetime(2023, 11, 25, 15, 0, 0),
        "attachments":  [{"filename": "project.pdf", "size_kb": 500}]
    },
    {
        "student_id":   7,
        "course_code":  "ME101",
        "semester":     "2023-ODD",
        "rating":       1,
        "comments":     "Very disappointing course.",
        "tags":         ["poor", "needs-improvement"],
        "submitted_at": datetime(2023, 11, 26, 10, 0, 0),
        "attachments":  []
    },
    {
        "student_id":   8,
        "course_code":  "CS103",
        "semester":     "2022-ODD",
        "rating":       4,
        "comments":     "Great examples. Concepts clear.",
        "tags":         ["good-examples", "clear", "challenging"],
        "submitted_at": datetime(2022, 12, 3, 12, 0, 0),
        "attachments":  []
    },
]

result = feedback.insert_many(sample_feedback)
print(f"\nTask 1: Inserted {len(result.inserted_ids)} documents")
print(f"Total documents: {feedback.count_documents({})}")

# ============================================================
# TASK 2: CRUD Operations
# ============================================================

print("\n--- Task 2: CRUD Operations ---")

# Query 65: READ — feedback where rating is 5
print("\nRating = 5 feedback:")
five_star = list(feedback.find({"rating": 5}, {"student_id": 1, "course_code": 1, "rating": 1, "_id": 0}))
for doc in five_star:
    print(f"  {doc}")

# Query 66: READ — CS101 feedback where tags contain 'challenging'
print("\nCS101 feedback tagged 'challenging':")
challenging = list(feedback.find(
    {"course_code": "CS101", "tags": "challenging"},
    {"student_id": 1, "course_code": 1, "rating": 1, "tags": 1, "_id": 0}
))
for doc in challenging:
    print(f"  {doc}")

# Query 67: READ — projection (specific fields only, no _id)
print("\nProjection (student_id, course_code, rating only):")
projected = list(feedback.find(
    {},
    {"student_id": 1, "course_code": 1, "rating": 1, "_id": 0}
))
for doc in projected[:3]:  # Show first 3
    print(f"  {doc}")
print(f"  ... and {len(projected) - 3} more")

# Query 68: UPDATE — add needs_review = True for rating < 3
update_result = feedback.update_many(
    {"rating": {"$lt": 3}},
    {"$set": {"needs_review": True}}
)
print(f"\nUpdated {update_result.modified_count} documents with needs_review = True")

# Query 69: UPDATE — push 'reviewed' tag to needs_review documents
push_result = feedback.update_many(
    {"needs_review": True},
    {"$push": {"tags": "reviewed"}}
)
print(f"Pushed 'reviewed' tag to {push_result.modified_count} documents")

# Query 70: DELETE — remove 2021-EVEN semester feedback
delete_result = feedback.delete_many({"semester": "2021-EVEN"})
print(f"Deleted {delete_result.deleted_count} documents from 2021-EVEN semester")
print(f"Documents remaining: {feedback.count_documents({})}")

# ============================================================
# TASK 3: Aggregation Pipeline
# ============================================================

print("\n--- Task 3: Aggregation Pipeline ---")

# Query 71 + 72: Pipeline — filter 2022-ODD, group, sort, project
pipeline1 = [
    # Stage 1: Filter to semester 2022-ODD
    {"$match": {"semester": "2022-ODD"}},

    # Stage 2: Group by course_code
    {"$group": {
        "_id":            "$course_code",
        "avg_rating":     {"$avg": "$rating"},
        "feedback_count": {"$sum": 1}
    }},

    # Stage 3: Sort by average rating descending
    {"$sort": {"avg_rating": DESCENDING}},

    # Stage 4: Project — rename and round avg_rating
    {"$project": {
        "course_code":      "$_id",
        "average_rating":   {"$round": ["$avg_rating", 1]},
        "feedback_count":   1,
        "_id":              0
    }}
]

print("\nCourse rating summary (2022-ODD semester):")
for doc in feedback.aggregate(pipeline1):
    print(f"  {doc}")

# Query 73: Tag frequency leaderboard using $unwind
pipeline2 = [
    # Deconstruct the tags array — each tag becomes a separate document
    {"$unwind": "$tags"},

    # Group by tag and count occurrences
    {"$group": {
        "_id":   "$tags",
        "count": {"$sum": 1}
    }},

    # Sort by count descending
    {"$sort": {"count": DESCENDING}},

    # Rename _id to tag
    {"$project": {
        "tag":   "$_id",
        "count": 1,
        "_id":   0
    }}
]

print("\nTag frequency leaderboard:")
for doc in feedback.aggregate(pipeline2):
    print(f"  {doc}")

# Query 74: Create index on course_code and check with explain
feedback.create_index([("course_code", ASCENDING)], name="idx_course_code")
print("\nIndex created on course_code")

# Verify index is used (IXSCAN should appear in the plan)
explain_result = feedback.find({"course_code": "CS101"}).explain()
stage = explain_result.get("queryPlanner", {}).get("winningPlan", {})
print(f"Query plan stage: {stage.get('stage', 'unknown')} (should be FETCH or IXSCAN)")

client.close()
print("\nMongoDB connection closed.")
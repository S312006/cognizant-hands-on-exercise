// ============================================================
// HANDS-ON 5 — MongoDB Document Modelling, CRUD & Aggregation
// Digital Nurture 5.0 | Module 3: Database Integration
// ============================================================


// ============================================================
// TASK 1: Create Collection and Insert Documents
// ============================================================

// Step 1: Switch to the database (creates it if not exists)
use college_nosql

// Step 2: Insert 10 feedback documents
db.feedback.insertMany([
  {
    student_id: 1,
    course_code: 'CS101',
    semester: '2022-ODD',
    rating: 5,
    comments: 'Excellent teaching! Highly recommended.',
    tags: ['challenging', 'well-structured'],
    submitted_at: new Date(),
    attachments: [{ filename: 'notes.pdf', size_kb: 240 }]
  },
  {
    student_id: 2,
    course_code: 'CS101',
    semester: '2022-ODD',
    rating: 4,
    comments: 'Good examples given in class.',
    tags: ['challenging', 'good-examples'],
    submitted_at: new Date(),
    attachments: []
  },
  {
    student_id: 3,
    course_code: 'CS101',
    semester: '2022-ODD',
    rating: 2,
    comments: 'Too fast paced. Hard to follow.',
    tags: ['fast-paced'],
    submitted_at: new Date(),
    attachments: []
  },
  {
    student_id: 4,
    course_code: 'CS102',
    semester: '2022-ODD',
    rating: 5,
    comments: 'Loved every lecture!',
    tags: ['well-structured', 'good-examples'],
    submitted_at: new Date(),
    attachments: [{ filename: 'slides.pdf', size_kb: 300 }]
  },
  {
    student_id: 5,
    course_code: 'CS102',
    semester: '2022-ODD',
    rating: 3,
    comments: 'Average experience overall.',
    tags: ['average'],
    submitted_at: new Date()
    // Note: No attachments field — MongoDB schema-less design allows this!
  },
  {
    student_id: 6,
    course_code: 'CS103',
    semester: '2021-EVEN',
    rating: 1,
    comments: 'Very poor teaching quality.',
    tags: ['boring'],
    submitted_at: new Date(),
    attachments: []
  },
  {
    student_id: 7,
    course_code: 'CS103',
    semester: '2022-ODD',
    rating: 4,
    comments: 'Quite informative and well explained.',
    tags: ['well-structured'],
    submitted_at: new Date(),
    attachments: []
  },
  {
    student_id: 8,
    course_code: 'CS101',
    semester: '2021-EVEN',
    rating: 3,
    comments: 'Okay course, could be better.',
    tags: ['average', 'challenging'],
    submitted_at: new Date(),
    attachments: []
  },
  {
    student_id: 9,
    course_code: 'CS104',
    semester: '2022-ODD',
    rating: 2,
    comments: 'Needs a lot of improvement.',
    tags: ['fast-paced'],
    submitted_at: new Date(),
    attachments: []
  },
  {
    student_id: 10,
    course_code: 'CS104',
    semester: '2022-ODD',
    rating: 5,
    comments: 'Best course I have ever taken!',
    tags: ['good-examples', 'well-structured'],
    submitted_at: new Date(),
    attachments: [{ filename: 'summary.pdf', size_kb: 150 }]
  }
])

// Step 3: Verify — should return 10
db.feedback.countDocuments()


// ============================================================
// TASK 2: CRUD Operations
// ============================================================

// Query 65 — READ: Find all documents where rating is 5
db.feedback.find({ rating: 5 })

// Query 66 — READ: Find CS101 feedback with 'challenging' tag
db.feedback.find({ course_code: 'CS101', tags: 'challenging' })

// Query 67 — READ: Projection — show only student_id, course_code, rating
db.feedback.find({}, { student_id: 1, course_code: 1, rating: 1, _id: 0 })

// Query 68 — UPDATE: Add needs_review:true to all documents with rating < 3
db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } }
)

// Query 69 — UPDATE: Push 'reviewed' tag to all needs_review documents
db.feedback.updateMany(
  { needs_review: true },
  { $push: { tags: 'reviewed' } }
)

// Query 70 — DELETE: Delete all documents from semester '2021-EVEN'
db.feedback.deleteMany({ semester: '2021-EVEN' })

// Verify after delete — should return 8
db.feedback.countDocuments()


// ============================================================
// TASK 3: Aggregation Pipeline
// ============================================================

// Pipeline 71 — Filter by semester, group by course, sort by avg rating
db.feedback.aggregate([
  { $match: { semester: '2022-ODD' } },
  {
    $group: {
      _id: '$course_code',
      avg_rating: { $avg: '$rating' },
      total_feedback: { $sum: 1 }
    }
  },
  { $sort: { avg_rating: -1 } }
])

// Pipeline 72 — Extend with $project to rename and round avg_rating
db.feedback.aggregate([
  { $match: { semester: '2022-ODD' } },
  {
    $group: {
      _id: '$course_code',
      avg_rating: { $avg: '$rating' },
      total_feedback: { $sum: 1 }
    }
  },
  { $sort: { avg_rating: -1 } },
  {
    $project: {
      _id: 1,
      average_rating: { $round: ['$avg_rating', 1] },
      total_feedback: 1
    }
  }
])

// Pipeline 73 — Tag frequency leaderboard using $unwind
db.feedback.aggregate([
  { $unwind: '$tags' },
  {
    $group: {
      _id: '$tags',
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])

// Pipeline 74 — Create index on course_code
db.feedback.createIndex({ course_code: 1 })

// Verify index is used — look for IXSCAN in output (not COLLSCAN)
db.feedback.find({ course_code: 'CS101' }).explain('executionStats')
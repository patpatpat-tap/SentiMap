-- SentiMap Posts Table Setup for Supabase
-- ==========================================
-- Run this SQL in your Supabase SQL Editor to create the table structure

CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT,
  full_text TEXT NOT NULL,
  created_date DATE,
  upvotes INTEGER DEFAULT 0,
  num_comments INTEGER DEFAULT 0,
  url TEXT,
  locations TEXT,
  comments_text TEXT,
  is_relevant BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on created_date for faster queries
CREATE INDEX idx_posts_created_date ON posts(created_date);

-- Create an index on is_relevant for filtering
CREATE INDEX idx_posts_is_relevant ON posts(is_relevant);

-- Enable RLS (Row Level Security) if needed
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows public read access (optional)
CREATE POLICY "Allow public read access" ON posts
  FOR SELECT TO anon, authenticated
  USING (TRUE);

-- Show confirmation
SELECT 'Posts table created successfully!' as status;

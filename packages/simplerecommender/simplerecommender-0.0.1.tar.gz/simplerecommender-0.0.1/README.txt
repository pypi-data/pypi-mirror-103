# simplerecommender

Recommending items for a specific existing user based on user rating and average rating per item

## Installation

Run the following to install:

```python
pip install simplerecommender
```

## Usage

```python
import simplerecommender

# get recommendations

simplerecommender.rec(df, genre_col, user_col, user, user_rating_col, avg_rating_col, sep=None)
```
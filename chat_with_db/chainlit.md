# Welcome to Blume DB! 🚀🤖

Hi there! 👋 This is [my (Prannay Kedia)](https://prannaykedia.com) implementation of the assignment for Blume VC's development internship. This chat bot interacts with a database (Postgres DB) and runs SQL queries from normal human text.

## Amazon Reviews Schema

This schema outlines the structure of the `amazon_reviews` table, detailing the data types and descriptions of each column.
| Column Name | Data Type | Description |
|-------------------|----------------|-----------------------------------------------------------------------------------------------|
| reviewerID | Text | Identifies the reviewer. |
| asin | Text | Identifies the product. |
| reviewerName | Text | Name of the reviewer. |
| helpful | Text | Indicates how helpful the review was. |
| reviewText | Text | Contains the review text. |
| overall | BigInt | Overall rating given by the reviewer. |
| summary | Text | Summary of the review. |
| unixReviewTime | BigInt | Unix timestamp of the review time. |
| reviewTime | Text | Review time in a different format. |

## Useful Links 🔗

- **Blume GPT:** Alternate solution where you can use AI to analyse your own CSV or Excel files [Blume GPT](https://blume-gpt.prannaykedia.com) 📚
- **Assignment One-pager:** Go through the one-pager for an in-depth discussion of the analysis [One Pager](https://discord.gg/k73SQ3FyUh) 💬

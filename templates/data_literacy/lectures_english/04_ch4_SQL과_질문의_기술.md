# Chapter 4: SQL and the Art of Asking Questions

No matter how well data is accumulated, it is useless if you can't pull out the answer you want. This chapter covers how to turn a vague curiosity like "what style is doing well?" into a precise question that a computer can actually answer. The tool for this is **SQL (Structured Query Language)**.

## Why Practitioners Need to Know SQL

Learning SQL does not mean you need to become a developer. The reason SQL matters in planning, marketing, and MD work is not the technical skill of writing code itself, but **the ability to translate your own hypothesis into a precise data request**.

If you hand the question "what's selling well these days?" directly to a data team, the data team has to ask back about the time period, the criterion (sales quantity or revenue), and the comparison group (overall, or by category). If this back-and-forth repeats, decision-making slows down. If you understand SQL syntax, you can organize your question into clear conditions from the start, and collaboration with the data team speeds up significantly.

## The Logic of Data Extraction

The core syntax of SQL maps directly onto the structure of a question.

- **SELECT**: What do you want to see (product name, sales quantity, revenue)
- **FROM**: What data will you look in (the sales history table)
- **WHERE**: What conditions will you narrow it down by (a specific season, a specific category)
- **GROUP BY**: What will you group the results by (by style, by size, by store)

For example, a request like "I want to see sales by size for the dress category this summer season" turns into a statement that aggregates (SELECT) sales quantity, grouped by size (GROUP BY), under the condition (WHERE) of dress and summer season, from the sales history table (FROM). Even without knowing the syntax, if you can answer these four questions yourself, you've already done half the work of a data request.

| SQL keyword | Form of question | This example |
| --- | --- | --- |
| SELECT | What do you want to see | Size, sales quantity |
| FROM | What data will you look in | Sales history table |
| WHERE | What conditions will you narrow by | Category = Dress, Season = Summer |
| GROUP BY | What will you group by | By size |

```sql
SELECT size, SUM(quantity) AS total_sold
FROM sales_history
WHERE category = '원피스' AND season = '여름'
GROUP BY size
ORDER BY total_sold DESC;
```

## Making Vague Requests Concrete

A sentence like "what style is selling well?" is easy to say casually, but data cannot answer it, because the following items are undecided.

- **Time period**: The last week, or the entire current season?
- **Metric**: Sales quantity, revenue, or sell-through rate relative to inventory?
- **Comparison group**: Compared to all products, the same category, or the same price range?

If you request data without deciding these three things, different people will come up with different answers, and getting different numbers for the same question erodes trust. Collaboration begins the moment a vague request is turned into concrete conditions. Change "a style that's doing well" into something like "the top 10 styles by sell-through rate relative to inventory over the last two weeks," and anyone who extracts the data will arrive at the same answer.

## Data Exercise: Bestsellers and Style-Level Sales Contribution

Let's think step by step through the process of pulling bestsellers from fashion transaction data.

1. Narrow the sales history table down using the analysis period as a condition (WHERE).
2. Sum sales quantity and revenue at the style level (GROUP BY, SELECT).
3. Sort the summed results in descending order of revenue (ORDER BY).
4. Decide the criterion for how many top items to select as bestsellers (LIMIT).

Taking this one step further, you can compute "sales contribution by style." Dividing each style's revenue by the total category revenue reveals how much weight a single style carries in overall performance. If this weight is overly concentrated in a particular style, that's a signal to also examine the risk of that style going out of stock.

| Style | Revenue (10,000 KRW) | Share within category |
| --- | --- | --- |
| Linen shirt dress | 3,200 | 32% |
| Pleated midi dress | 2,100 | 21% |
| Sum of the other 8 styles | 4,700 | 47% |

*Figure: A flowchart of the data extraction pipeline going from question to SQL query to result table*
![SQL question-query-result flowchart](/static/image/lectures/ch4_query_pipeline.png)

## Chapter Summary

- The value of SQL lies not in coding skill but in the ability to translate a hypothesis into a precise question.
- SELECT-FROM-WHERE-GROUP BY represents what, from where, under what conditions, and how to group.
- A vague request like "a style that's doing well" can only be answered with data once the time period, metric, and comparison group are decided.
- Clearly defining conditions means the same result comes out no matter who extracts the data, which increases trust in collaboration.
- Bestseller analysis must look beyond simple sales volume to contribution relative to the whole and concentration risk.

## Explore Further: Assignments Using Generative AI

1. **Convert natural language into SQL**: Create a vague question of the kind covered in this chapter, such as "show me sales by size for the dress category this summer season, sorted by revenue," tell a generative AI the table structure (what columns are in the sales history table), and ask it to write the SQL query. Check one by one whether the SELECT-FROM-WHERE-GROUP BY structure the AI created fully reflects the conditions of your question.
2. **Practice making vague requests concrete**: Ask a generative AI to "turn the vague question 'what style is doing well?' into 3 concrete questions that can be answered with data," and check whether the time period, metric, and comparison group needed for each question are clear.
3. **Verify interpretation of query results**: Given the results of a bestseller extraction query created by a generative AI (either run on sample data or an example result the AI created), ask it to "judge whether revenue in this result is overly concentrated in a particular style," and verify by calculating it yourself whether the AI's reasoning holds up.

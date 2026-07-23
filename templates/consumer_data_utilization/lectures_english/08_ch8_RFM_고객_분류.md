# Chapter 8: Segmenting Customers With RFM

Almost everyone has received a text, chat message, or email from a fashion store recommending a product. Outside a handful of large retailers, most stores don't analyze each customer individually — instead, they group customers by a few criteria and target recommendations at the group level. This chapter covers **RFM analysis**, the most widely used method for segmenting customers this way.

> **Something to think about**
> Between "a customer who visits our store often but rarely buys anything" and "a customer who visits rarely but buys a lot each time," which one is the more important customer? Do you think there's a single correct answer?

## Learning Objectives

By the end of this unit, you will be able to:

- Explain what each letter in RFM (Recency, Frequency, Monetary) means.
- Understand why practitioners often simplify three-dimensional RFM down to two-dimensional FM.
- Explain the basic idea of k-means clustering and how the boundary used to split groups changes the result.
- Connect a customer segmentation result to real marketing, such as a VIP strategy.

## Key Terms

- **RFM**: A customer segmentation framework named after its three initials — Recency, Frequency, Monetary.
- **Recency**: The gap between today and a customer's last visit or purchase.
- **Frequency**: How many times a customer visited or purchased within a defined period.
- **Monetary**: The total amount a customer spent within a defined period.

## What RFM Is

RFM segments customers based on their behavior. Suppose a store learns that its highest-revenue customers are 46 to 60 years old, middle-income, have small households, and shop online frequently — the store could then focus marketing on people in their 40s and 50s living in similar neighborhoods. Conversely, if a low-revenue but recently active customer segment turns out to favor a particular car brand and live in a particular area, the store might try promotions targeted at that region or car-owner community.

Breaking down the three letters:

- **R (Recency)**: The gap between today and the customer's last visit or purchase.
- **F (Frequency)**: How often the customer visited the store within a defined period.
- **M (Monetary)**: How much the customer spent within a defined period.

You might wonder why variables like age, location, gender, or purchased category aren't included from the start. Two reasons. Adding more segmentation criteria makes each group's traits harder to explain, and it increases both the data volume and the analytical complexity, often demanding more computing power than is warranted. If a recommendation system is being introduced for the first time, it's better to start with RFM and add variables later as the need arises.

## Simplifying to Two Dimensions: FM

RFM is technically a three-dimensional analysis, but in practice it's often explained using only two dimensions — **F (frequency) and M (monetary)** — to avoid confusion. Here's how:

1. Rank Frequency and Monetary values into quintiles, giving each customer a rank from 1 to 5 on each.
2. A customer ranked 1st in Frequency and 5th in Monetary can be intuitively read as a "picky big spender" who visits rarely but spends a lot each time; a customer ranked 5th in Frequency and 1st in Monetary reads as someone who visits often but spends little.
3. Plotting these two ranks on a 2D scatter plot — Frequency on the x-axis, Monetary on the y-axis — reveals that in most stores, mid-level spenders cluster densely, while the top-right (high frequency, high spend) and bottom-left (low frequency, low spend) corners hold relatively few customers.

*Figure: a scatter plot with Frequency on the x-axis and Monetary on the y-axis, showing low-frequency, low-spend customers clustered in the bottom left, thinning out toward the top right.*
![RFM Frequency-Monetary scatter plot](/static/image/lectures/cdu_ch8_rfm_scatter.png)

## Splitting Customers With K-Means Clustering

Once the FM preprocessing is done, customers are split into groups using the widely known **k-means clustering** algorithm — or a marketer can simply draw the dividing lines by hand. Where those lines get drawn matters a great deal, because completely different insights emerge depending on the choice.

- Dividing diagonally from the origin surfaces a group whose loyalty rises the closer they sit to the top right.
- Dividing along separate axes can isolate a specific behavior pattern, such as "visits often but rarely actually buys."

When there's no clear rule for how many groups to use, a common practical approach is to start with 4 or 5 and adjust after looking at the result. More groups allow finer-grained recommendations per customer, but that also means preparing more recommendation menus and more computing resources — a trade-off worth weighing.

## A Caution When Interpreting Clusters

After segmenting customers with RFM, the next step is usually to look at each cluster's demographic traits — preferred car type, home region, and so on — to "explain" what the cluster represents. A common question comes up at this point: "If we're going to do that anyway, why not just include demographic variables in the segmentation criteria from the start?" The answer is: you can, but it isn't recommended. Pushing the number of segmentation criteria past two tends to make each cluster's character rapidly harder to explain. Try to explain a cluster by age, and its revenue-contribution pattern gets muddier; try to explain it by region, and the age grouping gets muddier — adding more criteria tends to trap you in a loop where fixing one explanation breaks another.

If what a marketer actually wants is demographic criteria — age, region — rather than RFM, the better order is to segment by those demographic criteria first, then use RFM to explain the traits of each resulting group.

## Application: Pulling VIPs Toward VVIP

RFM segmentation results serve as the basis for planning events tailored to customer traits or for product recommendations. A common application splits top-revenue customers into two tiers, VVIP and VIP, then recommends products VVIPs bought to VIPs — nudging VIPs toward VVIP-level spending. It's worth remembering, though, that the same data can lead to completely different conclusions depending on the analyst's or marketer's point of view. One team might focus on nurturing high-potential customers; another might focus on retaining already-loyal ones. The analysis only points a direction — choosing which direction to take is a human call.

## Short Activity: Rank FM by Hand

Below are five customers' visit counts (F) and spending (M) over the last three months. Rank each on a scale of 1 to 5 (1 = highest).

| Customer | Visits (F) | Spend (M) | F rank | M rank |
|---|---|---|---|---|
| A | 12 | 850,000 |  |  |
| B | 3 | 1,200,000 |  |  |
| C | 15 | 90,000 |  |  |
| D | 1 | 50,000 |  |  |
| E | 8 | 400,000 |  |  |

Once ranked, mark which customer looks closest to a "picky big spender" (low frequency, high spend) and which looks closest to a "loyal" customer (high frequency, high spend).

## Chapter Summary

- RFM segments customers using three behavioral metrics: recency, frequency, and monetary value.
- In practice, three-dimensional RFM is often simplified to two-dimensional FM to ease interpretation and reduce computational cost.
- After ranking FM, customers are split into groups using k-means clustering or boundaries a marketer draws by hand.
- Pushing past two segmentation criteria makes clusters hard to explain, which is why segmenting by RFM and explaining with demographics (or the reverse) is the recommended division of labor.
- The same RFM data can lead to entirely different strategies depending on the analyst's or marketer's intent.

## Comprehension Check

1. Write out what each letter of RFM stands for.
2. Why do practitioners often simplify RFM down to two-dimensional FM in practice?
3. What problem arises from pushing the number of segmentation criteria (variables) too high?
4. Explain the RFM strategy for nudging a VIP toward VVIP status.

<details>
<summary>Show answers and explanations</summary>

1. R is recency (the gap between today and the last visit or purchase), F is frequency (visit or purchase count within a defined period), and M is monetary (total spend within a defined period).
2. A three-dimensional graph is harder to read intuitively and can cause confusion, so viewing the customer distribution across just the F and M axes is easier to understand.
3. Explaining each cluster's traits as one coherent story becomes difficult — explaining with one variable tends to weaken the explanatory power of another, repeatedly.
4. Split top-revenue customers into VVIP and VIP tiers, then recommend products VVIPs bought to VIPs, aiming to pull VIP spending up toward the VVIP level.

</details>

## Try It With Generative AI

1. **Practice RFM on synthetic data**: Ask a generative AI to "create a table of RFM data for 10 hypothetical customers," then rank F and M by hand using the method from this chapter and sketch out rough clusters.
2. **Review a cluster interpretation**: Ask a generative AI to "explain the pitfalls of describing RFM-based customer clusters using age and location," and compare its answer with this chapter's caution on interpreting clusters.

> **Keep in mind**
> There's no single correct number of groups or boundary values for RFM segmentation. Treat any "ideal number of groups" a generative AI proposes as one opinion to consider, and adjust it yourself to fit the actual business goal.

## Next Chapter

This chapter covered segmenting customers by behavioral data. The next chapter turns back to products, covering how image data is turned into numbers to automatically find visually similar products — the logic behind image-similarity recommendation.

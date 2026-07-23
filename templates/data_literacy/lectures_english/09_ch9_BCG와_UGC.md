# Chapter 9: Brand Generated Content and User Generated Content

The data surrounding a fashion brand can be divided into what the brand creates and what consumers create. This chapter examines the nature of **BGC (Brand Generated Content)** and **UGC (User Generated Content)** respectively, and what value emerges when the two are used together.

## Brand-Centered Data

Category classifications, master attributes, official runway show footage, and lookbooks are all data created intentionally by the brand. The defining characteristic of this data is **consistency and control**. Color codes, material information, and size notation are recorded precisely according to rules the brand has set, and lookbooks and editorial photoshoots are the result of carefully staging the image the brand wants to convey.

Thanks to this order, brand data is well suited to uses where accuracy matters, such as product search, inventory management, and official catalogs. However, because it reflects what the brand intends, this data alone has a limitation: it's hard to know how consumers actually perceive and use the product from it.

## User-Centered Data

By contrast, wear photos customers post, styling reviews, product reviews, and behavioral logs like clicks and purchases show, as-is, how consumers actually use products. UGC reveals cases where customers style a product differently from what the brand suggested, or wear it in situations the brand never anticipated.

The strength of UGC is **authenticity**. It captures real body types, real lighting, and real everyday life, which builds trust with other consumers. In exchange, its free-form nature and inconsistent quality make it hard to organize into structured information, and there's a risk that the opinions of a small number of highly active users become overrepresented.

## Trust and Reach

The two types of data have different characteristics in terms of trust and reach.

- **Brand-generated data**: Accurate and consistent, but may be biased in a direction favorable to the brand. Its reach depends on the brand's marketing budget and channels.
- **User-generated data**: Realistic and captures diverse perspectives, but can be biased toward users of a certain disposition. It sometimes reaches much further than expected through word-of-mouth and sharing.

When analyzing trends, you need to understand the purpose and bias behind each type of data and mix them appropriately. Looking only at brand data misses actual consumer reaction, while looking only at UGC can skew toward a subset of voices without the full picture.

| | BGC (Brand Generated Content) | UGC (User Generated Content) |
| --- | --- | --- |
| Who creates it | The brand | Consumers |
| Strength | Accuracy, consistency | Authenticity, trustworthiness |
| Weakness | Can be biased toward the brand's perspective | Hard to structure, can be biased toward certain users |
| Representative examples | Official lookbooks, category classifications, size charts | Wear reviews, styling feedback, hashtag posts |

## Combining the Two Types of Data

When accurate product information (brand data) is combined with real preference data (user data), the quality of search and recommendation improves noticeably. For example, if the accurate category the brand has defined, "minimal trench coat," is linked to tags users freely attach in real life, like "daily look" or "office look," then typing "a coat good for wearing to work" into a search box can surface related products.

In this way, brand data provides an accurate skeleton, and UGC plays the role of adding the flesh of real-life context onto that skeleton. The better the work of connecting the two types of data — tag mapping, review analysis, image similarity calculation — the closer recommendation and search come to natural language.

*Figure: A structural diagram showing the brand-defined category (skeleton) connecting with user tags and reviews (context) to merge into a single search result*
![BGC-UGC combination structure diagram](/static/image/lectures/ch9_bgc_ugc_combination.png)

## Fashion Business Case: The Gap Between Runway and Street Fashion

There is often a gap between the runway trends of a fashion show (brand-generated data) and the street fashion people actually wear (user-generated data). A silhouette introduced on the runway often appears in a transformed form in consumers' actual wardrobes.

To bridge this gap with data, you can organize the color, silhouette, and material information of a runway collection into structured data, while also analyzing styling photos and hashtags posted on social media to compare which elements consumers actually adopted and which elements they transformed. Through this comparison, a brand can use data to judge which experimental elements from the runway to bring into its commercial line.

## Real-World Case: Glossier's Community-Based Product Development

The beauty brand Glossier is well known for gathering product ideas from the reader community of "Into The Gloss," the blog it ran before founding the company. A representative example is asking specific questions like "what is your dream cleanser?" and gathering opinions across hundreds of comments, then reflecting them in an actual product launch (such as the Milky Jelly Cleanser).

This demonstrates the power of user-generated data (UGC) covered in this chapter. The actual language and needs of users — things that cannot be known from the categories and specs the brand defines (BGC) alone — are revealed through the UGC of community comments and social posts, creating a cycle where this in turn feeds back into product planning and marketing copy.

## Chapter Summary

- Brand Generated Content (BGC) is accurate and consistent, but can be biased toward the brand's perspective.
- User Generated Content (UGC) is realistic and diverse, but is hard to structure and can be biased toward certain users.
- Because the two types of data differ in purpose and bias, both trust and reach must be considered when using them.
- Connecting accurate brand information with real preference data improves the quality of search and recommendation.
- The gap between runway trends and consumers' actual style can be narrowed by analyzing BGC and UGC together.

## Explore Further: Assignments Using Generative AI

1. **Request UGC text analysis**: Gather 10-20 actual review or feedback texts about a specific product (either captured yourself or from publicly available reviews), ask a generative AI to "analyze the keywords and sentiment (positive/negative) that repeat across these reviews," and compare the results with the product description originally provided by the brand (BGC).
2. **Design a crowdsourcing question**: Referring to Glossier's "what is your dream cleanser?" case, ask a generative AI to "create 5 open-ended questions that could be posed to a customer community to get ideas for a new product," and compare which questions are more specific and easier to get answers to.
3. **Compare the runway-street gap**: Ask a generative AI to summarize recent season runway trend keywords, then compare them with street fashion photos or posts you've actually observed on social media, and directly analyze "which elements of the runway were actually adopted by consumers."

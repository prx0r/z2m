# Prototype notes

This intentionally demonstrates the **correct abstraction level**:

- one `advisor.html`
- one `core.js`
- one `styles.css`
- one `configs.js`

A new vertical is a new object in `configs.js` until real demand proves that it deserves deeper product logic.

The demo is rule-based and uses illustrative recommendations. Before production:

1. Replace result data with verified supplier offers.
2. Add server-side analytics.
3. Connect conversion button to lead/cart/quote endpoint.
4. Add model reasoning only after deterministic compatibility filtering.
5. Add image/video generation only after a message/offer proves conversion.

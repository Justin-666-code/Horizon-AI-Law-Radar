# Implementation Plan

1. Update the personal preference order and digest labels.
   - Put foundations and research before product output.
   - Prioritize product-engineering articles ahead of general technology news.
   - Make product-engineering the largest technical output bucket without
     increasing the daily item cap.

2. Update profile judgment.
   - `ai-foundations`: reinforce current coursework and avoid model-training
     recommendations.
   - `ai-research`: require a capability-boundary, evaluation, or product
     judgment takeaway.
   - `tech-blog` and `tech-news`: apply the product-engineering lens.
   - `law-governance`: classify safety governance, intellectual property, and
     digital government independently.

3. Update tests and module documentation.
   - Assert the new profile order and engineering quota.
   - Describe the route-aware responsibilities in the profile maps.

4. Validate.
   - Compile `data/config.json`.
   - Run the personal-radar tests.
   - Inspect the compiled order, limits, and profile display names.

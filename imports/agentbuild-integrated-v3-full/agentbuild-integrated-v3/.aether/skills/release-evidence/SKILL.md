# Release Evidence

A release is a chain of evidence:
blueprint -> task -> diff/build result -> preview -> deterministic gate -> optional deploy -> production fetch.

A pass requires no unresolved critical/high verified finding. Warnings must be preserved in the receipt. Never silently drop failed attempts; they are useful future training/lineage data for FinalBuilds.

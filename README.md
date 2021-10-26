# Turn.io Content Tags & Card API integration

This replit shows how to use the data export API and the cards API to find out which bits of content where sent to which clients having which labels.

# How to run this Repl.it

[![Run on Repl.it](https://repl.it/badge/github/turnhub/turnio-content-tags-replit)](https://repl.it/github/turnhub/turnio-content-tags-replit)

1. Click the `Run on Repl.it` button above and install this example into your Repl.it workspace.
2. Get a Turn token and add it as a secret called `TOKEN` in Repl.it
3. Optionally, set the `TOKEN` variable if your Turn instance is on a private cloud. If not, it will default to connect to `https://whatsapp.turn.io`.
5. Send a message to your number by selecting a card in the Turn UI which has one or more labels assigned.
6. Run this replit.

It will do the following:

1. Use the Data Export API to retrieve messages from the last 24 hours
2. It will select outbound messages which have a `card_uuid`
3. Find the relevant card for the UUID using `/v1/cards/<uuid>`
4. Print a summary of cards used and labels on said card.

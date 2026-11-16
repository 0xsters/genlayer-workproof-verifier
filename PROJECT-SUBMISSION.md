# GenLayer Portal: Projects submission, ready to paste

Form: Submit Contribution, Contribution Type "Builder", Category "Projects" (Project Explorer application).
Weekly capacity shown on the form: 2 Project slots, resets Monday 00:00 UTC. Points range: 20 - 4,000 pts.

## 01 Identity

- Logo: upload `logo.png` from this project folder (1024 x 1024 PNG).
- Project Name: WorkProof
- Primary Tag: choose the closest available option to "Infrastructure" (if that is absent, "Developer Tools").
- Tag 1: AI
- Tag 2: Oracles

## 02 One-liner (max 100 characters)

Work acceptance checked by validator consensus, not by one reviewer or a screenshot.

## 03 Description (max 1,000 characters)

WorkProof is a reusable acceptance primitive for work that is paid or credited on delivery: bounties, contribution programs, grants, and agent marketplaces. The party offering work registers a task in the WorkProof Intelligent Contract: a title, acceptance criteria in plain language, a public evidence URL, and a pass score. When the work is done, anyone can resolve the task. GenLayer validators independently fetch the evidence page and grade it against every criterion. The verdict is stored on chain only when validators agree under a custom equivalence rule: the verdict must match exactly, the score must be within 15 points, and the criteria met count within 1. The result is one shared, public verdict that both sides can point to, instead of an argument over screenshots. This page is the working app: it creates tasks, resolves them, and reads verdicts directly from the deployed contract on GenLayer Studionet, with 9 passing direct tests and full documentation in the GitHub repository.

## 04 Demo video (optional)

Leave empty, or add later.

## 05 Write the exact path (how-to steps)

Step 1, heading: "Open the app and connect a wallet"
Instruction: "Open https://workproof-seven.vercel.app and click Connect wallet. If the GenLayer Studionet network (chain 61999) is not in your wallet yet, the app offers to add it. Approve the connection."

Step 2, heading: "Register a piece of work"
Instruction: "Fill in the title, the acceptance criteria in plain language, the public evidence URL, and a pass score between 1 and 100, then click Create task and confirm the transaction in your wallet. Wait until the app reports the task as registered."

Step 3, heading: "Resolve the task"
Instruction: "In the Tasks list, find the task and click Resolve this task, then confirm in your wallet. Validators fetch the evidence page and grade it. Finalization can take a minute or more."

Step 4, heading: "Read the verdict"
Instruction: "Reload the page. The task now shows the stored verdict: accepted, rejected, or inconclusive, with the score, how many criteria were met, and a short summary written by the validators."

## 06 Prove the path works

Expected verification outcome (max 500 characters):

After following the steps, the Tasks list shows the new task as resolved. Its verdict box shows the verdict, the score, the criteria met count, and a summary. The same verdict is stored in the contract at 0xD974a24a033714a64987539EF13986f63E51d426 on GenLayer Studionet and can be checked in the explorer link below and by calling get_task with the task id. Before any task is created, the counter at the top of the app reads the live total from the contract.

Contract link 1 (optional): https://explorer-studio.genlayer.com/address/0xD974a24a033714a64987539EF13986f63E51d426

## 07 Project links

- Website (required): https://workproof-seven.vercel.app
- GitHub: https://github.com/0xsters/genlayer-workproof-verifier

## Evidence and Supporting Information

- Add Evidence, type "GitHub Repository": https://github.com/0xsters/genlayer-workproof-app
  (This is the app repository. Do NOT use the verifier repository here: its URL was already used by the Intelligent Contracts submission, and the portal rejects it with "This URL has already been submitted." The 07 GitHub field keeps the verifier repository, which is a different field and a different URL.)

Then tick "I'm not a robot" and click Submit Contribution.

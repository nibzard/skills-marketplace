# Claude Thread Publisher - Example Prompts

This document contains example prompts for using the **claude-thread-publisher** skill.

## Publishing Threads

### Basic Publishing
> "Publish this Claude Code session as a shareable link."

> "Create a permalink for this conversation I can share with my team."

> "Export this conversation to a static HTML page that I can share."

> "Turn this thread into a shareable webpage."

> "Publish this conversation and give me a URL I can send to others."

### Publishing with Context
> "I want to share this debugging session with my colleague. Can you publish it as a link?"

> "This conversation contains some great solutions. Could you publish it so I can reference it later?"

> "Make this thread public so the whole team can see how we solved this problem."

> "Can you help me document this conversation by publishing it as a shareable page?"

## Managing Published Threads

### Deleting Threads
> "Delete the public link you created for this thread."

> "Remove the published version of this conversation."

> "I want to unpublish this thread. Can you delete the shareable link?"

> "Take down the public version of this conversation."

### Updating Threads
> "Update the published permalink for this thread with the new messages."

> "This conversation has continued since we published it. Can you update the public link?"

> "Re-publish this thread with the latest changes."

> "The published version is outdated. Can you update it with our current discussion?"

## Listing and Information

### Listing Published Threads
> "Show me all the threads I've published."

> "List all of my published Claude Code conversations."

> "What conversations have I made public with this tool?"

> "Can you show me a history of threads I've shared?"

### Checking Status
> "Is this conversation already published?"

> "Does this thread have a public link?"

> "Have we shared this discussion before?"

> "What's the status of the published version of this thread?"

## Advanced Usage

### Custom Publishing
> "Publish this as a public thread (not private)."

> "Create a shareable link for just the first part of this conversation."

> "Publish this conversation but make sure it's private."

> "Can you publish this with a specific title?"

### Bulk Operations
> "Clean up any old published threads I don't need anymore."

> "Delete all published threads from this project."

> "Show me published threads from the past week."

> "Are there any orphaned gists from this tool that I should clean up?"

### Troubleshooting
> "I'm getting an error when trying to publish. Can you help?"

> "The publishing failed. What went wrong?"

> "I can't find the session file for this conversation."

> "The GitHub token seems to be missing. Can you help me set it up?"

## Workflow Examples

### Development Documentation Workflow
> "I just finished implementing the user authentication feature. Can you publish this entire development session so I can reference it in our team documentation?"

> "This debugging session was really informative. Can you create a shareable link for the knowledge base?"

> "We've figured out the solution to this complex problem. Let's publish this conversation for the whole team to learn from."

### Code Review Workflow
> "Can you publish our code review discussion so we can share the decisions with other team members?"

> "This architectural decision conversation should be documented. Can you make it shareable?"

> "Let's publish this refactoring discussion so the new team members can understand our approach."

### Knowledge Sharing Workflow
> "I want to share this helpful conversation with the community. Can you publish it?"

> "This troubleshooting guide would be useful for others. Can you make it public?"

> "Can you turn this technical discussion into a shareable resource?"

## Integration Examples

### Project Management
> "After this planning session, can you publish it and add the link to our project documentation?"

> "Let's document this sprint retrospective by publishing it as a shareable page."

> "Publish this requirements discussion so stakeholders can review it."

### Team Collaboration
> "Can you publish our brainstorming session so absent team members can catch up?"

> "Let's share this solution discussion with the other development team."

> "Publish our technical debate so we can get input from the architecture team."

### Personal Knowledge Management
> "I want to save this conversation for future reference. Can you publish it for me?"

> "This was a really productive discussion. Can you create a permanent link for it?"

> "Let me publish this so I can easily find it later and share with new team members."

## Error Recovery Examples

### When Publishing Fails
> "The publish failed. Can you try again with a different approach?"

> "I got a GitHub API error. Can you help me troubleshoot the publishing?"

> "The session file isn't found. Can you help me locate it and publish this thread?"

### When Deleting Fails
> "The deletion didn't work. Can you help me remove the published thread?"

> "I can't seem to delete this published link. What should I do?"

> "The gist deletion failed. Can you help me clean up this published thread?"

## Contextual Examples

### Starting a Publishing Session
> "Before we continue, could you publish the conversation so far?"

> "Let's pause here and publish what we've discussed so I can share progress."

> "At this milestone, can you create a shareable link to our discussion?"

### Ending a Publishing Session
> "Now that we're done, can you publish this complete conversation?"

> "As a final step, let's make this discussion shareable."

> "Before we wrap up, can you publish this conversation for the records?"

## Multi-step Workflow Examples

### Full Documentation Workflow
1. "First, let's publish this design discussion."
2. "Now that we have the implementation, can you update the published link with the complete solution?"
3. "Finally, can you give me both the design link and the implementation link so I can document both phases?"

### Progressive Publishing Workflow
1. "Let's publish our initial approach to this problem."
2. "After this new insight, can you update the published thread with our revised solution?"
3. "Now that we've completed it, can you update the thread one final time with the full implementation?"

### Review and Refine Workflow
1. "Publish this draft solution so I can get feedback."
2. "After incorporating the feedback, can you update the published link?"
3. "Now that it's approved, can you make it public for the team?"

## Sample Outputs

### Successful Publishing Response
```
✅ Thread published successfully!
🔗 Permalink: https://gistpreview.github.io/?abcdef1234567890
📄 Gist URL: https://gist.github.com/abcdef1234567890
🆔 Gist ID: abcdef1234567890
🔐 Thread Hash: a1b2c3d4e5f67890abcdef1234567890
```

### Update Response
```
✅ Thread updated successfully!
🔗 Permalink: https://gistpreview.github.io/?abcdef1234567890 (unchanged)
📄 Gist URL: https://gist.github.com/abcdef1234567890
🆔 Gist ID: abcdef1234567890
🔄 Action: Updated existing gist with new content
```

### Deletion Response
```
✅ Thread deletion completed successfully.
🗑️ Deleted Gist: abcdef1234567890
📝 Thread Hash: a1b2c3d4e5f67890abcdef1234567890
✅ Local index updated
```

## Troubleshooting Prompts

### Authentication Issues
> "I'm getting a GitHub token error. Can you help me set up authentication?"

> "The skill says I need a GitHub PAT. What should I do?"

> "How do I create the GitHub token needed for publishing?"

### Session Detection Issues
> "The tool can't find my current session. What should I check?"

> "I'm in a project directory but it says no session is found. Why?"

> "How does the skill detect which conversation I want to publish?"

### Network/Connectivity Issues
> "The publishing failed due to network issues. Can you retry?"

> "I'm having connectivity problems with GitHub. What should I do?"

> "The GitHub API seems to be down. Can I try again later?"
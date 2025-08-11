import { openai } from "@ai-sdk/openai"
import { streamText } from "ai"

// IMPORTANT! Set the runtime to edge
export const runtime = "edge"

export async function POST(req: Request) {
  const { messages } = await req.json()

  // Add a system prompt to guide the AI
  const systemPrompt = `You are an expert social media marketing assistant for Tim Hortons.
  Your goal is to help users refine their social media posts.
  Be friendly, helpful, and embody the Tim Hortons brand values: community, warmth, Canadian pride.
  When a user provides a post or asks for help with one, offer constructive feedback, suggest improvements,
  help brainstorm ideas, or check for brand alignment.
  Keep your responses concise and actionable.`

  const result = await streamText({
    model: openai("gpt-4o"), // You can change the model as needed
    system: systemPrompt,
    messages,
  })

  return result.toAIStreamResponse()
}

"use client"

import { useState, useRef, useEffect, type FormEvent } from "react"
import { useChat, type Message } from "ai/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Paperclip, Send, MessageSquare, X, CornerDownLeft, Bot, User } from "lucide-react"
import { cn } from "@/lib/utils"

export function AiChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } = useChat({
    api: "/api/chat",
  })
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTo({
        top: scrollAreaRef.current.scrollHeight,
        behavior: "smooth",
      })
    }
  }, [messages])

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  const toggleChat = () => {
    setIsOpen(!isOpen)
  }

  const CustomFormEvent = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!input.trim()) return
    handleSubmit(e)
  }

  return (
    <>
      <Button
        onClick={toggleChat}
        className={cn(
          "fixed bottom-6 right-6 w-16 h-16 rounded-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-xl transition-all duration-300 ease-in-out transform hover:scale-110 z-50",
          isOpen && "opacity-0 scale-0",
        )}
        aria-label="Toggle AI Chat"
      >
        <MessageSquare size={28} />
      </Button>

      {isOpen && (
        <div className="fixed bottom-6 right-6 w-[380px] h-[calc(100vh-100px)] max-h-[600px] bg-white rounded-xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden z-50 transition-all duration-300 ease-in-out animate-in slide-in-from-bottom-5 fade-in">
          {/* Header */}
          <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Avatar className="w-8 h-8">
                <AvatarImage src="/placeholder.svg?height=32&width=32" />
                <AvatarFallback className="bg-red-600 text-white text-xs">AI</AvatarFallback>
              </Avatar>
              <div>
                <h3 className="font-semibold text-slate-800 text-sm">AI Post Assistant</h3>
                <p className="text-xs text-slate-500">Online</p>
              </div>
            </div>
            <Button variant="ghost" size="icon" onClick={toggleChat} className="text-slate-500 hover:text-slate-700">
              <X size={20} />
            </Button>
          </div>

          {/* Messages Area */}
          <ScrollArea className="flex-1 p-4 space-y-4" ref={scrollAreaRef}>
            {messages.length === 0 && !isLoading && (
              <div className="text-center text-slate-500 text-sm py-8">
                <Bot size={32} className="mx-auto mb-2 text-red-500" />
                <p>Hi there! How can I help you with your Tim Hortons post today?</p>
                <p className="text-xs mt-1">e.g., "Review this post for me" or "Give me ideas for a holiday post."</p>
              </div>
            )}
            {messages.map((m: Message) => (
              <div key={m.id} className={cn("flex items-start space-x-3 py-2", m.role === "user" ? "justify-end" : "")}>
                {m.role === "assistant" && (
                  <Avatar className="w-8 h-8 flex-shrink-0">
                    <AvatarImage src="/placeholder.svg?height=32&width=32" />
                    <AvatarFallback className="bg-red-600 text-white text-xs">AI</AvatarFallback>
                  </Avatar>
                )}
                <div
                  className={cn(
                    "p-3 rounded-lg max-w-[75%] text-sm",
                    m.role === "user"
                      ? "bg-red-600 text-white rounded-br-none"
                      : "bg-slate-100 text-slate-800 rounded-bl-none",
                  )}
                >
                  {m.content.split("\n").map((line, i) => (
                    <span key={i}>
                      {line}
                      {i !== m.content.split("\n").length - 1 && <br />}
                    </span>
                  ))}
                </div>
                {m.role === "user" && (
                  <Avatar className="w-8 h-8 flex-shrink-0">
                    <AvatarImage src="/placeholder.svg?height=32&width=32" />
                    <AvatarFallback className="bg-slate-300 text-slate-700 text-xs">
                      <User size={16} />
                    </AvatarFallback>
                  </Avatar>
                )}
              </div>
            ))}
            {isLoading && messages.length > 0 && messages[messages.length - 1].role === "user" && (
              <div className="flex items-start space-x-3 py-2">
                <Avatar className="w-8 h-8 flex-shrink-0">
                  <AvatarImage src="/placeholder.svg?height=32&width=32" />
                  <AvatarFallback className="bg-red-600 text-white text-xs">AI</AvatarFallback>
                </Avatar>
                <div className="p-3 rounded-lg bg-slate-100 text-slate-800 rounded-bl-none">
                  <div className="flex space-x-1 items-center">
                    <span className="w-2 h-2 bg-slate-400 rounded-full animate-pulse delay-75"></span>
                    <span className="w-2 h-2 bg-slate-400 rounded-full animate-pulse delay-150"></span>
                    <span className="w-2 h-2 bg-slate-400 rounded-full animate-pulse delay-300"></span>
                  </div>
                </div>
              </div>
            )}
          </ScrollArea>

          {error && (
            <div className="p-4 text-xs text-red-600 bg-red-50 border-t border-red-200">
              Error: {error.message}. Please try again.
            </div>
          )}

          {/* Input Area */}
          <div className="p-4 border-t border-slate-200 bg-slate-50">
            <form onSubmit={CustomFormEvent} className="flex items-center space-x-2">
              <Button variant="ghost" size="icon" className="text-slate-500 hover:text-slate-700 flex-shrink-0">
                <Paperclip size={20} />
              </Button>
              <Input
                ref={inputRef}
                value={input}
                onChange={handleInputChange}
                placeholder="Ask about your post..."
                className="flex-1 bg-white border-slate-300 focus:border-red-500 focus:ring-red-500/20"
                disabled={isLoading && messages.length > 0 && messages[messages.length - 1].role === "user"}
              />
              <Button
                type="submit"
                size="icon"
                className="bg-red-600 hover:bg-red-700 text-white flex-shrink-0"
                disabled={isLoading && messages.length > 0 && messages[messages.length - 1].role === "user"}
              >
                {isLoading && messages.length > 0 && messages[messages.length - 1].role === "user" ? (
                  <CornerDownLeft size={20} className="animate-ping" />
                ) : (
                  <Send size={20} />
                )}
              </Button>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

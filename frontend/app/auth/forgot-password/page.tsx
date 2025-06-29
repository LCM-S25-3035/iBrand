"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Sparkles, ArrowLeft, CheckCircle2 } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function ForgotPasswordPage() {
  const [showDemo, setShowDemo] = useState(false)
  const [email, setEmail] = useState("")
  const [submitted, setSubmitted] = useState(false)
  const router = useRouter()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, this would send a password reset email
    // For demo purposes, we'll just show a success message
    setSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-50/30 flex flex-col">
      <div className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <Link href="/auth/login" className="flex items-center space-x-2 group">
            <ArrowLeft className="w-5 h-5 text-slate-500 group-hover:text-red-600 transition-colors" />
            <span className="text-slate-500 group-hover:text-red-600 transition-colors">Back to login</span>
          </Link>
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center shadow-lg shadow-red-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-red-600 to-red-700 bg-clip-text text-transparent">
              IBrand
            </span>
          </div>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-red-700 rounded-2xl blur-xl opacity-10 animate-pulse"></div>
            <div className="relative bg-white backdrop-blur-sm border border-slate-200 rounded-2xl shadow-2xl shadow-red-500/5 p-8">
              {!submitted ? (
                <>
                  <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-slate-900 mb-2">Reset your password</h1>
                    <p className="text-slate-600">We'll send you a link to reset your password</p>
                  </div>

                  {showDemo && (
                    <Alert className="mb-6 bg-red-50 border-red-200 text-red-800">
                      <AlertDescription>
                        <strong>Demo Info:</strong> This is a demo, so no actual email will be sent. In a real
                        application, this would send a password reset link to your email.
                      </AlertDescription>
                    </Alert>
                  )}

                  <form className="space-y-6" onSubmit={handleSubmit}>
                    <div className="space-y-2">
                      <Label htmlFor="email" className="text-slate-700">
                        Email
                      </Label>
                      <Input
                        id="email"
                        type="email"
                        placeholder="you@company.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="bg-white border-slate-300 text-slate-900 placeholder:text-slate-400 focus:border-red-500 focus:ring-red-500/20"
                      />
                    </div>

                    <div className="flex justify-between items-center">
                      <div></div>
                      <Button
                        type="button"
                        variant="ghost"
                        className="text-sm text-red-600 hover:text-red-800"
                        onClick={() => setShowDemo(!showDemo)}
                      >
                        Demo info
                      </Button>
                    </div>

                    <Button
                      type="submit"
                      className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20 py-6"
                    >
                      Send reset link
                    </Button>
                  </form>
                </>
              ) : (
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <CheckCircle2 className="w-8 h-8 text-green-600" />
                  </div>
                  <h2 className="text-2xl font-bold text-slate-900 mb-2">Check your email</h2>
                  <p className="text-slate-600 mb-6">
                    We've sent a password reset link to <span className="font-medium">{email}</span>
                  </p>
                  <Button
                    onClick={() => router.push("/auth/login")}
                    className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20"
                  >
                    Back to login
                  </Button>
                </div>
              )}

              {!submitted && (
                <div className="mt-6 text-center">
                  <p className="text-slate-600">
                    Remember your password?{" "}
                    <Link href="/auth/login" className="text-red-600 hover:text-red-800 font-medium">
                      Back to login
                    </Link>
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
          <p>© 2024 IBrand. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link href="#" className="hover:text-red-600">
              Terms
            </Link>
            <Link href="#" className="hover:text-red-600">
              Privacy
            </Link>
            <Link href="#" className="hover:text-red-600">
              Contact
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Sparkles, ArrowLeft, Eye, EyeOff, CheckCircle2 } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function SignupPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [showDemo, setShowDemo] = useState(false)
  const router = useRouter()

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, this would register with a backend
    // For demo purposes, we'll just redirect to the dashboard
    router.push("/")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-50/30 flex flex-col">
      <div className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <Link href="/landing" className="flex items-center space-x-2 group">
            <ArrowLeft className="w-5 h-5 text-slate-500 group-hover:text-red-600 transition-colors" />
            <span className="text-slate-500 group-hover:text-red-600 transition-colors">Back to home</span>
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
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-slate-900 mb-2">Create your account</h1>
                <p className="text-slate-600">Start your 14-day free trial, no credit card required</p>
              </div>

              {showDemo && (
                <Alert className="mb-6 bg-red-50 border-red-200 text-red-800">
                  <AlertDescription>
                    <strong>Demo Info:</strong> This is a demo, so you can use any information to sign up. In a real
                    application, this would register with a backend.
                  </AlertDescription>
                </Alert>
              )}

              <form className="space-y-6" onSubmit={handleSignup}>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="first-name" className="text-slate-700">
                      First name
                    </Label>
                    <Input
                      id="first-name"
                      placeholder="John"
                      className="bg-white border-slate-300 text-slate-900 placeholder:text-slate-400 focus:border-red-500 focus:ring-red-500/20"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="last-name" className="text-slate-700">
                      Last name
                    </Label>
                    <Input
                      id="last-name"
                      placeholder="Doe"
                      className="bg-white border-slate-300 text-slate-900 placeholder:text-slate-400 focus:border-red-500 focus:ring-red-500/20"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email" className="text-slate-700">
                    Work email
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@company.com"
                    className="bg-white border-slate-300 text-slate-900 placeholder:text-slate-400 focus:border-red-500 focus:ring-red-500/20"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="company" className="text-slate-700">
                    Company name
                  </Label>
                  <Input
                    id="company"
                    placeholder="Your Company"
                    className="bg-white border-slate-300 text-slate-900 placeholder:text-slate-400 focus:border-red-500 focus:ring-red-500/20"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password" className="text-slate-700">
                    Password
                  </Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      className="bg-white border-slate-300 text-slate-900 placeholder:text-slate-400 focus:border-red-500 focus:ring-red-500/20 pr-10"
                    />
                    <button
                      type="button"
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-2">
                    <div className="flex items-center space-x-2 text-xs">
                      <CheckCircle2 className="w-3.5 h-3.5 text-green-500" />
                      <span className="text-slate-600">At least 8 characters</span>
                    </div>
                    <div className="flex items-center space-x-2 text-xs">
                      <CheckCircle2 className="w-3.5 h-3.5 text-green-500" />
                      <span className="text-slate-600">One uppercase letter</span>
                    </div>
                    <div className="flex items-center space-x-2 text-xs">
                      <CheckCircle2 className="w-3.5 h-3.5 text-green-500" />
                      <span className="text-slate-600">One number</span>
                    </div>
                    <div className="flex items-center space-x-2 text-xs">
                      <CheckCircle2 className="w-3.5 h-3.5 text-green-500" />
                      <span className="text-slate-600">One special character</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-start space-x-2">
                  <Checkbox id="terms" className="mt-1" />
                  <Label htmlFor="terms" className="text-sm text-slate-600 font-normal">
                    I agree to the{" "}
                    <Link href="#" className="text-red-600 hover:text-red-800">
                      Terms of Service
                    </Link>{" "}
                    and{" "}
                    <Link href="#" className="text-red-600 hover:text-red-800">
                      Privacy Policy
                    </Link>
                  </Label>
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
                  Create account
                </Button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-slate-600">
                  Already have an account?{" "}
                  <Link href="/auth/login" className="text-red-600 hover:text-red-800 font-medium">
                    Sign in
                  </Link>
                </p>
              </div>

              <div className="mt-8 pt-6 border-t border-slate-200">
                <div className="flex items-center justify-center space-x-4">
                  <Button
                    variant="outline"
                    className="flex-1 border-slate-300 text-slate-700 hover:bg-slate-100 hover:text-slate-900"
                  >
                    <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                        fill="#4285F4"
                      />
                      <path
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                        fill="#34A853"
                      />
                      <path
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                        fill="#FBBC05"
                      />
                      <path
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                        fill="#EA4335"
                      />
                    </svg>
                    Google
                  </Button>
                  <Button
                    variant="outline"
                    className="flex-1 border-slate-300 text-slate-700 hover:bg-slate-100 hover:text-slate-900"
                  >
                    <svg
                      className="w-5 h-5 mr-2"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path d="M13.397 20.997v-8.196h2.765l.411-3.209h-3.176V7.548c0-.926.258-1.56 1.587-1.56h1.684V3.127A22.336 22.336 0 0 0 14.201 3c-2.444 0-4.122 1.492-4.122 4.231v2.355H7.332v3.209h2.753v8.202h3.312z" />
                    </svg>
                    Facebook
                  </Button>
                </div>
              </div>
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

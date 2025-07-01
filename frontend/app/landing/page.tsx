import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  ArrowRight,
  Sparkles,
  TrendingUp,
  Zap,
  BarChart3,
  Globe,
  MessageSquare,
  CheckCircle2,
  ChevronRight,
} from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-50/30">
      {/* Header */}
      <header className="border-b border-white/20 bg-white/90 backdrop-blur-xl sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-red-600 to-red-700 rounded-xl flex items-center justify-center shadow-lg shadow-red-500/20">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-red-600 to-red-700 bg-clip-text text-transparent">
                  IBrand
                </h1>
                <p className="text-sm text-slate-600">AI-Powered Social Intelligence</p>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <nav className="flex items-center space-x-6">
                <Link
                  href="#features"
                  className="text-sm font-medium text-slate-600 hover:text-red-600 transition-colors"
                >
                  Features
                </Link>
                <Link
                  href="#how-it-works"
                  className="text-sm font-medium text-slate-600 hover:text-red-600 transition-colors"
                >
                  How It Works
                </Link>
                <Link
                  href="#testimonials"
                  className="text-sm font-medium text-slate-600 hover:text-red-600 transition-colors"
                >
                  Testimonials
                </Link>
                <Link
                  href="#pricing"
                  className="text-sm font-medium text-slate-600 hover:text-red-600 transition-colors"
                >
                  Pricing
                </Link>
              </nav>
              <div className="flex items-center space-x-3">
                <Button variant="ghost" className="text-slate-600 hover:text-red-600" asChild>
                  <Link href="/auth/login">Log in</Link>
                </Button>
                <Button
                  className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20"
                  asChild
                >
                  <Link href="/auth/signup">Sign up</Link>
                </Button>
              </div>
            </div>
            <Button variant="ghost" className="md:hidden text-slate-600">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="4" x2="20" y1="12" y2="12" />
                <line x1="4" x2="20" y1="6" y2="6" />
                <line x1="4" x2="20" y1="18" y2="18" />
              </svg>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-[40%] -right-[10%] w-[70%] h-[70%] bg-red-600 opacity-5 rounded-full blur-[120px]"></div>
          <div className="absolute -bottom-[30%] -left-[10%] w-[70%] h-[70%] bg-red-600 opacity-5 rounded-full blur-[120px]"></div>
        </div>
        <div className="container mx-auto px-6 relative">
          <div className="max-w-4xl mx-auto text-center mb-16">
            <Badge className="mb-6 bg-red-100 text-red-700 border-red-200 backdrop-blur-sm py-1.5 px-4 rounded-full">
              <Sparkles className="w-3.5 h-3.5 mr-1.5" />
              AI-Powered Social Media Intelligence
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6 leading-tight">
              Transform News into Engaging Brand Content
            </h1>
            <p className="text-lg md:text-xl text-slate-600 mb-8 leading-relaxed">
              IBrand uses AI to monitor trending news and instantly create on-brand social media content that drives
              engagement, builds community, and strengthens your brand identity.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <Button
                className="w-full sm:w-auto text-base bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20 px-8 py-6"
                asChild
              >
                <Link href="/auth/signup">
                  Get Started Free
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
              </Button>
              <Button
                variant="outline"
                className="w-full sm:w-auto text-base border-slate-300 text-slate-700 hover:bg-slate-100 px-8 py-6"
                asChild
              >
                <Link href="#demo">Watch Demo</Link>
              </Button>
            </div>
          </div>

          {/* Hero Image */}
          <div className="relative mx-auto max-w-5xl">
            <div className="absolute inset-0 bg-gradient-to-t from-white via-transparent to-transparent z-10"></div>
            <img
              src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop&q=80"
              alt="IBrand Dashboard"
              className="w-full h-auto rounded-xl shadow-2xl shadow-red-500/10 border border-slate-200"
            />
            <div className="absolute -bottom-5 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-red-600 to-red-700 px-6 py-3 rounded-full shadow-lg shadow-red-500/20 backdrop-blur-sm">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                <span className="text-white font-medium">2,500+ brands using IBrand</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Brands Section */}
      <section className="py-16 bg-white/50 backdrop-blur-sm border-y border-slate-200">
        <div className="container mx-auto px-6">
          <p className="text-center text-slate-600 mb-10">Trusted by innovative brands worldwide</p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 items-center justify-items-center opacity-70">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Tim_Hortons_logo.svg/320px-Tim_Hortons_logo.svg.png"
              alt="Tim Hortons"
              className="h-8 object-contain"
            />
            <img
              src="https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/320px-Starbucks_Corporation_Logo_2011.svg.png"
              alt="Starbucks"
              className="h-8 object-contain"
            />
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_NIKE.svg/320px-Logo_NIKE.svg.png"
              alt="Nike"
              className="h-8 object-contain"
            />
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Spotify_logo_with_text.svg/320px-Spotify_logo_with_text.svg.png"
              alt="Spotify"
              className="h-8 object-contain"
            />
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/320px-Airbnb_Logo_B%C3%A9lo.svg.png"
              alt="Airbnb"
              className="h-8 object-contain"
            />
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Uber_logo_2018.svg/320px-Uber_logo_2018.svg.png"
              alt="Uber"
              className="h-8 object-contain"
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 relative">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-[20%] -left-[10%] w-[50%] h-[50%] bg-red-600 opacity-5 rounded-full blur-[120px]"></div>
        </div>
        <div className="container mx-auto px-6 relative">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <Badge className="mb-4 bg-red-100 text-red-700 border-red-200 backdrop-blur-sm py-1 px-3 rounded-full">
              Features
            </Badge>
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6">
              Everything you need to dominate social media
            </h2>
            <p className="text-slate-600">
              IBrand combines AI-powered content generation with real-time news monitoring to help your brand stay
              relevant and engaging.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 hover:shadow-red-500/10 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center mb-6 shadow-lg shadow-red-500/20">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Trend Monitoring</h3>
              <p className="text-slate-600 mb-4">
                Real-time monitoring of industry news, trends, and conversations relevant to your brand.
              </p>
              <ul className="space-y-2">
                {["Real-time news feeds", "Customizable filters", "Relevance scoring", "Competitor tracking"].map(
                  (item, i) => (
                    <li key={i} className="flex items-center text-sm text-slate-600">
                      <CheckCircle2 className="w-4 h-4 mr-2 text-red-500" />
                      {item}
                    </li>
                  ),
                )}
              </ul>
            </div>

            {/* Feature 2 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 hover:shadow-red-500/10 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center mb-6 shadow-lg shadow-red-500/20">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">AI Content Generation</h3>
              <p className="text-slate-600 mb-4">
                Transform trending news into on-brand social media posts optimized for engagement.
              </p>
              <ul className="space-y-2">
                {[
                  "Platform-specific formatting",
                  "Brand voice matching",
                  "Image generation",
                  "Hashtag optimization",
                ].map((item, i) => (
                  <li key={i} className="flex items-center text-sm text-slate-600">
                    <CheckCircle2 className="w-4 h-4 mr-2 text-red-500" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* Feature 3 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 hover:shadow-red-500/10 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center mb-6 shadow-lg shadow-red-500/20">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Analytics & Insights</h3>
              <p className="text-slate-600 mb-4">
                Track performance and optimize your content strategy with detailed analytics.
              </p>
              <ul className="space-y-2">
                {["Engagement metrics", "Audience insights", "Content performance", "Competitive analysis"].map(
                  (item, i) => (
                    <li key={i} className="flex items-center text-sm text-slate-600">
                      <CheckCircle2 className="w-4 h-4 mr-2 text-red-500" />
                      {item}
                    </li>
                  ),
                )}
              </ul>
            </div>

            {/* Feature 4 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 hover:shadow-red-500/10 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center mb-6 shadow-lg shadow-red-500/20">
                <Globe className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Multi-Platform Publishing</h3>
              <p className="text-slate-600 mb-4">
                Publish content across all major social platforms with a single click.
              </p>
              <ul className="space-y-2">
                {[
                  "Instagram, Twitter, LinkedIn",
                  "Scheduling tools",
                  "Cross-platform analytics",
                  "Content calendar",
                ].map((item, i) => (
                  <li key={i} className="flex items-center text-sm text-slate-600">
                    <CheckCircle2 className="w-4 h-4 mr-2 text-red-500" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* Feature 5 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 hover:shadow-red-500/10 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center mb-6 shadow-lg shadow-red-500/20">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Brand Voice Training</h3>
              <p className="text-slate-600 mb-4">
                Train our AI to perfectly match your brand's unique voice and style.
              </p>
              <ul className="space-y-2">
                {["Voice customization", "Style guidelines", "Tone adjustment", "Continuous learning"].map(
                  (item, i) => (
                    <li key={i} className="flex items-center text-sm text-slate-600">
                      <CheckCircle2 className="w-4 h-4 mr-2 text-red-500" />
                      {item}
                    </li>
                  ),
                )}
              </ul>
            </div>

            {/* Feature 6 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 hover:shadow-red-500/10 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center mb-6 shadow-lg shadow-red-500/20">
                <MessageSquare className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Community Management</h3>
              <p className="text-slate-600 mb-4">
                AI-powered responses to comments and messages that maintain your brand voice.
              </p>
              <ul className="space-y-2">
                {["Auto-responses", "Sentiment analysis", "Priority flagging", "Engagement tracking"].map((item, i) => (
                  <li key={i} className="flex items-center text-sm text-slate-600">
                    <CheckCircle2 className="w-4 h-4 mr-2 text-red-500" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-24 bg-red-50 backdrop-blur-sm border-y border-slate-200 relative">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute bottom-[20%] -right-[10%] w-[50%] h-[50%] bg-red-600 opacity-5 rounded-full blur-[120px]"></div>
        </div>
        <div className="container mx-auto px-6 relative">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <Badge className="mb-4 bg-red-100 text-red-700 border-red-200 backdrop-blur-sm py-1 px-3 rounded-full">
              How It Works
            </Badge>
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6">Simple, powerful, and effective</h2>
            <p className="text-slate-600">
              IBrand streamlines your social media workflow with a simple three-step process that saves time and drives
              results.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 relative">
            <div className="hidden md:block absolute top-1/2 left-1/4 right-1/4 h-0.5 bg-gradient-to-r from-transparent via-red-500 to-transparent transform -translate-y-1/2"></div>

            {/* Step 1 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 relative z-10">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-red-500/20 mx-auto">
                <span className="text-white font-bold">1</span>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3 text-center">Monitor Trends</h3>
              <p className="text-slate-600 text-center">
                Our AI constantly scans news sources, social media, and industry publications to identify relevant
                trending topics for your brand.
              </p>
            </div>

            {/* Step 2 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 relative z-10">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-red-500/20 mx-auto">
                <span className="text-white font-bold">2</span>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3 text-center">Generate Content</h3>
              <p className="text-slate-600 text-center">
                Select a trending topic and our AI instantly creates on-brand social media posts optimized for each
                platform you use.
              </p>
            </div>

            {/* Step 3 */}
            <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-xl p-6 shadow-lg shadow-red-500/5 relative z-10">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-red-500/20 mx-auto">
                <span className="text-white font-bold">3</span>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3 text-center">Publish & Analyze</h3>
              <p className="text-slate-600 text-center">
                Review, edit if needed, and publish directly to your social platforms. Track performance and optimize
                future content.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Case Study Section */}
      <section className="py-24 relative">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-[30%] -right-[10%] w-[50%] h-[50%] bg-red-600 opacity-5 rounded-full blur-[120px]"></div>
        </div>
        <div className="container mx-auto px-6 relative">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <Badge className="mb-4 bg-red-100 text-red-700 border-red-200 backdrop-blur-sm py-1 px-3 rounded-full">
              Case Study
            </Badge>
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6">How Tim Hortons drives engagement</h2>
            <p className="text-slate-600">
              See how Tim Hortons uses IBrand to create timely, relevant content that resonates with their Canadian
              audience.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <img
                src="https://images.unsplash.com/photo-1579389083078-4e7018379f7e?w=600&h=500&fit=crop&q=80"
                alt="Tim Hortons Case Study"
                className="w-full h-auto rounded-xl shadow-2xl shadow-red-500/10 border border-slate-200"
              />
            </div>
            <div className="space-y-6">
              <div className="flex items-center space-x-3 mb-2">
                <img
                  src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Tim_Hortons_logo.svg/120px-Tim_Hortons_logo.svg.png"
                  alt="Tim Hortons Logo"
                  className="w-12 h-12 rounded-full"
                />
                <h3 className="text-2xl font-bold text-slate-900">Tim Hortons</h3>
              </div>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-lg p-4">
                  <p className="text-3xl font-bold text-slate-900">47%</p>
                  <p className="text-sm text-slate-600">Engagement Increase</p>
                </div>
                <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-lg p-4">
                  <p className="text-3xl font-bold text-slate-900">3.2x</p>
                  <p className="text-sm text-slate-600">Content Output</p>
                </div>
                <div className="bg-white backdrop-blur-sm border border-slate-200 rounded-lg p-4">
                  <p className="text-3xl font-bold text-slate-900">68%</p>
                  <p className="text-sm text-slate-600">Time Saved</p>
                </div>
              </div>

              <p className="text-slate-600">
                "IBrand has transformed how we respond to current events. We can now create timely, on-brand content
                that resonates with our Canadian audience in minutes instead of days. The AI perfectly captures our
                brand voice while keeping our content fresh and relevant."
              </p>

              <div className="flex items-center space-x-3 pt-4">
                <img
                  src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=48&h=48&fit=crop&q=80"
                  alt="Marketing Director"
                  className="w-12 h-12 rounded-full"
                />
                <div>
                  <p className="font-medium text-slate-900">Sarah Johnson</p>
                  <p className="text-sm text-slate-600">Director of Social Media, Tim Hortons</p>
                </div>
              </div>

              <Button
                className="mt-6 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20"
                asChild
              >
                <Link href="#case-studies">
                  Read Full Case Study
                  <ChevronRight className="ml-2 w-4 h-4" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-br from-red-50 to-red-100/50 backdrop-blur-sm border-y border-red-100 relative">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-[30%] left-[30%] w-[40%] h-[40%] bg-red-600 opacity-5 rounded-full blur-[120px]"></div>
        </div>
        <div className="container mx-auto px-6 relative">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl md:text-5xl font-bold text-slate-900 mb-6 leading-tight">
              Ready to transform your social media strategy?
            </h2>
            <p className="text-xl text-red-700 mb-10 leading-relaxed">
              Join thousands of brands using IBrand to create engaging, timely content that drives results.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <Button
                className="w-full sm:w-auto text-base bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white shadow-lg shadow-red-500/20 px-8 py-6"
                asChild
              >
                <Link href="/auth/signup">
                  Start Your Free Trial
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
              </Button>
              <Button
                variant="outline"
                className="w-full sm:w-auto text-base border-red-300 text-red-700 hover:bg-red-100 px-8 py-6"
                asChild
              >
                <Link href="/contact">Talk to Sales</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white py-16 border-t border-slate-200">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-12">
            <div>
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-red-600 to-red-700 rounded-xl flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-red-600 to-red-700 bg-clip-text text-transparent">
                    IBrand
                  </h1>
                </div>
              </div>
              <p className="text-slate-600 mb-6">AI-powered social media intelligence for forward-thinking brands.</p>
              <div className="flex space-x-4">
                <a href="#" className="text-slate-400 hover:text-red-600">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" />
                  </svg>
                </a>
                <a href="#" className="text-slate-400 hover:text-red-600">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                  </svg>
                </a>
                <a href="#" className="text-slate-400 hover:text-red-600">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                </a>
              </div>
            </div>

            <div>
              <h3 className="text-slate-900 font-semibold mb-4">Product</h3>
              <ul className="space-y-3">
                {["Features", "Pricing", "Case Studies", "Testimonials", "API"].map((item, i) => (
                  <li key={i}>
                    <Link href="#" className="text-slate-600 hover:text-red-600 transition-colors">
                      {item}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-slate-900 font-semibold mb-4">Company</h3>
              <ul className="space-y-3">
                {["About", "Blog", "Careers", "Press", "Partners"].map((item, i) => (
                  <li key={i}>
                    <Link href="#" className="text-slate-600 hover:text-red-600 transition-colors">
                      {item}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-slate-900 font-semibold mb-4">Resources</h3>
              <ul className="space-y-3">
                {["Documentation", "Help Center", "Community", "Webinars", "Privacy"].map((item, i) => (
                  <li key={i}>
                    <Link href="#" className="text-slate-600 hover:text-red-600 transition-colors">
                      {item}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-200 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-slate-500 text-sm mb-4 md:mb-0">© 2024 IBrand. All rights reserved.</p>
            <div className="flex space-x-6">
              <Link href="#" className="text-slate-500 hover:text-red-600 text-sm">
                Terms of Service
              </Link>
              <Link href="#" className="text-slate-500 hover:text-red-600 text-sm">
                Privacy Policy
              </Link>
              <Link href="#" className="text-slate-500 hover:text-red-600 text-sm">
                Cookie Policy
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

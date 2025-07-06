"use client";

import { useState, useMemo } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sparkles,
  TrendingUp,
  Clock,
  Eye,
  Share2,
  Download,
  RefreshCw,
  Zap,
  Search,
  Filter,
  BarChart3,
  Calendar,
  MapPin,
  Heart,
} from "lucide-react";
import { AiChatWidget } from "@/components/ai-chat-widget";

import { useGetNewsQuery } from "../store/api/newsApi";
import { useGeneratePostMutation } from "../store/api/generatePostApi";

// Mock trending news data focused on tariffs and trade
const trendingNews = [
  {
    id: 1,
    title: "US Announces New 25% Tariffs on Chinese Electric Vehicles",
    source: "Reuters",
    category: "Trade Policy",
    readTime: "4 min read",
    views: "45.2K",
    trending: true,
    publishedAt: "2024-01-15T10:30:00Z",
    summary:
      "Biden administration implements sweeping tariffs on Chinese EVs, citing national security concerns and unfair trade practices.",
    image:
      "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=250&fit=crop",
    tags: ["tariffs", "china", "electric-vehicles", "trade-war"],
    url: "https://reuters.com/article",
  },
  {
    id: 2,
    title: "European Union Considers Retaliatory Tariffs on US Steel Imports",
    source: "Financial Times",
    category: "International Trade",
    readTime: "3 min read",
    views: "32.8K",
    trending: true,
    publishedAt: "2024-01-14T14:20:00Z",
    summary:
      "EU trade officials debate imposing counter-tariffs following US steel import restrictions, escalating transatlantic trade tensions.",
    image:
      "https://images.unsplash.com/photo-1565793298595-6a879b1d9492?w=400&h=250&fit=crop",
    tags: ["eu", "steel", "tariffs", "trade-relations"],
    url: "https://reuters.com/article",
  },
  {
    id: 3,
    title:
      "Coffee Import Tariffs Could Increase Prices by 15% Across North America",
    source: "Bloomberg",
    category: "Agriculture",
    readTime: "5 min read",
    views: "38.5K",
    trending: true,
    publishedAt: "2024-01-13T09:15:00Z",
    summary:
      "New trade restrictions on coffee imports from South America may significantly impact coffee prices, affecting major chains and local cafes.",
    image:
      "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400&h=250&fit=crop",
    tags: ["coffee", "agriculture", "imports", "tariffs", "prices"],
    url: "https://reuters.com/article",
  },
  {
    id: 4,
    title:
      "Canada Strengthens Local Food Supply Chain Amid Trade Uncertainties",
    source: "CBC News",
    category: "Canadian Business",
    readTime: "6 min read",
    views: "29.1K",
    trending: true,
    publishedAt: "2024-01-12T16:45:00Z",
    summary:
      "Canadian food companies pivot to domestic suppliers as international trade tensions create supply chain vulnerabilities.",
    image:
      "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400&h=250&fit=crop",
    tags: ["canada", "food-supply", "local-suppliers", "trade"],
    url: "https://reuters.com/article",
  },
  {
    id: 5,
    title: "Dairy Tariff Protections Boost Canadian Farmers' Revenue by 22%",
    source: "Globe and Mail",
    category: "Agriculture",
    readTime: "4 min read",
    views: "19.7K",
    trending: false,
    publishedAt: "2024-01-11T11:30:00Z",
    summary:
      "Supply management system and tariff protections help Canadian dairy farmers maintain competitive pricing and quality standards.",
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=250&fit=crop",
    tags: ["canada", "dairy", "farmers", "supply-management"],
    url: "https://reuters.com/article",
  },
  {
    id: 6,
    title:
      "Maple Syrup Exports Surge as Trade Policies Favor Canadian Products",
    source: "National Post",
    category: "Canadian Business",
    readTime: "3 min read",
    views: "24.3K",
    trending: false,
    publishedAt: "2024-01-10T13:20:00Z",
    summary:
      "Canadian maple syrup producers see record exports as favorable trade agreements and tariff structures boost international demand.",
    image:
      "https://media.istockphoto.com/id/538184814/photo/maple-syrup-in-glass-bottle-on-wooden-table.jpg?s=612x612&w=0&k=20&c=otZW1nqNfVGroXScQR3jG3wwZYe28IWqufZw94lHHnA=",
    tags: ["maple-syrup", "exports", "canada", "trade-agreements"],
    url: "https://reuters.com/article",
  },
];

// Tim Hortons branded generated posts
const mockGeneratedPosts = {
  1: {
    platform: "LinkedIn",
    content:
      "🇨🇦 While trade tensions rise globally, Tim Hortons remains committed to what we do best - serving Canadians with pride! ☕\n\n🌟 Our strength comes from:\n• 60+ years of Canadian heritage\n• Supporting local suppliers coast-to-coast\n• Building communities, one cup at a time\n• Always True North strong and free\n\nIn uncertain times, we're your reliable Canadian comfort. What's your favorite Tims memory?\n\n#TimHortons #Canada #ProudlyCanadian #CommunityFirst #AlwaysFresh",
    hashtags: [
      "#TimHortons",
      "#Canada",
      "#ProudlyCanadian",
      "#CommunityFirst",
      "#AlwaysFresh",
    ],
    image:
      "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&h=400&fit=crop",
  },
  2: {
    platform: "Instagram",
    content:
      "🍁 Trade wars? We're fighting with kindness, one double-double at a time! ☕❤️\n\nWhile the world gets complicated, we keep it simple:\n✅ Fresh coffee, baked daily\n✅ Supporting Canadian communities\n✅ Bringing people together\n✅ Always here for you\n\nThat's the Tim Hortons way! 🇨🇦\n\n#TimsFamily #CanadianPride #CoffeeLovers #CommunityLove #AlwaysThere",
    hashtags: [
      "#TimsFamily",
      "#CanadianPride",
      "#CoffeeLovers",
      "#CommunityLove",
      "#AlwaysThere",
    ],
    image:
      "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&h=400&fit=crop",
  },
  3: {
    platform: "Twitter",
    content:
      "☕ Coffee prices rising due to tariffs? \n\nAt Tim Hortons, we're doubling down on our commitment to affordable, quality coffee for all Canadians! 🇨🇦\n\n✨ Same great taste\n✨ Same fair prices\n✨ Same Canadian values\n\nBecause everyone deserves their daily Tims! ❤️\n\n#TimHortons #AffordableCoffee #CanadianValues",
    hashtags: ["#TimHortons", "#AffordableCoffee", "#CanadianValues"],
    image:
      "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600&h=400&fit=crop",
  },
  4: {
    platform: "LinkedIn",
    content:
      "🇨🇦 PROUD MOMENT: While global supply chains face uncertainty, Tim Hortons continues to champion Canadian suppliers! 🌾\n\n📈 Our commitment:\n• 80% of ingredients sourced locally\n• Supporting 1,200+ Canadian farms\n• Creating 15,000+ jobs coast-to-coast\n• Investing $2.5B annually in Canadian communities\n\nWhen you choose Tims, you're choosing Canada. Together, we're stronger! 💪\n\n#TimHortons #BuyCanadian #LocalSuppliers #CommunityInvestment #ProudlyCanadian",
    hashtags: [
      "#TimHortons",
      "#BuyCanadian",
      "#LocalSuppliers",
      "#CommunityInvestment",
      "#ProudlyCanadian",
    ],
    image:
      "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&h=400&fit=crop",
  },
  5: {
    platform: "Instagram",
    content:
      "🥛 Supporting Canadian dairy farmers isn't just good business - it's who we are! 🇨🇦\n\nEvery Tim Hortons coffee is made with:\n✅ 100% Canadian dairy\n✅ Fresh, local ingredients\n✅ Love for our communities\n✅ Pride in our heritage\n\nTaste the difference that Canadian quality makes! ☕❤️\n\n#CanadianDairy #FarmToTable #QualityFirst #TimsFamily #LocalSupport",
    hashtags: [
      "#CanadianDairy",
      "#FarmToTable",
      "#QualityFirst",
      "#TimsFamily",
      "#LocalSupport",
    ],
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=600&h=400&fit=crop",
  },
  6: {
    platform: "Twitter",
    content:
      "🍁 Just like our maple syrup exports are booming, Tim Hortons is spreading Canadian warmth worldwide! 🌍\n\n✨ From coast to coast to coast\n✨ Now in 13+ countries\n✨ Same Canadian hospitality everywhere\n\nTaking a piece of Canada with us wherever we go! 🇨🇦☕\n\n#TimHortons #GlobalCanada #MapleProud",
    hashtags: ["#TimHortons", "#GlobalCanada", "#MapleProud"],
    image:
      "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600&h=400&fit=crop",
  },
};

const categories = [
  "All",
  "Trade Policy",
  "International Trade",
  "Agriculture",
  "Canadian Business",
  "Technology",
];
const sortOptions = [
  "Most Recent",
  "Most Popular",
  "Trending First",
  "Alphabetical",
];

export default function IBrandDashboard() {
  const { data: apiNews, isLoading, error } = useGetNewsQuery();
  const [generatePost, { isLoading: isPostLoading }] =
    useGeneratePostMutation();

  const combinedNews = useMemo(() => {
    if (!apiNews) return trendingNews;

    const transformedApiNews = apiNews.map((item, index) => ({
      id: index + 7,
      title: item.title,
      source: item.source,
      category: "Canadian Business", // or map from your API if you have it
      readTime: "6 min read", // optional
      views: "45.2K", // optional
      trending: true, // optional
      publishedAt: item.published_at,
      summary: item.summary,
      image:
        "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=250&fit=crop", // optional
      tags: item.tags,
      url: item.url,
    }));

    console.log(transformedApiNews);

    return [...trendingNews, ...transformedApiNews];
  }, [apiNews]);

  const [selectedNews, setSelectedNews] = useState<number | null>(null);
  const [generatedPost, setGeneratedPost] = useState<any>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [sortBy, setSortBy] = useState("Most Recent");

  const filteredNews = useMemo(() => {
    let filtered = combinedNews;

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(
        (news) =>
          news.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          news.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
          news.tags.some((tag) =>
            tag.toLowerCase().includes(searchQuery.toLowerCase())
          )
      );
    }

    // Filter by category
    if (selectedCategory !== "All") {
      filtered = filtered.filter((news) => news.category === selectedCategory);
    }

    // Sort
    switch (sortBy) {
      case "Most Popular":
        filtered = [...filtered].sort(
          (a, b) =>
            Number.parseFloat(b.views.replace("K", "")) -
            Number.parseFloat(a.views.replace("K", ""))
        );
        break;
      case "Trending First":
        filtered = [...filtered].sort(
          (a, b) => (b.trending ? 1 : 0) - (a.trending ? 1 : 0)
        );
        break;
      case "Alphabetical":
        filtered = [...filtered].sort((a, b) => a.title.localeCompare(b.title));
        break;
      default: // Most Recent
        filtered = [...filtered].sort(
          (a, b) =>
            new Date(b.publishedAt).getTime() -
            new Date(a.publishedAt).getTime()
        );
    }

    return filtered;
  }, [searchQuery, selectedCategory, sortBy, isLoading]);

  const handleSelectNews = (newsId: number) => {
    console.log(newsId);

    setSelectedNews(newsId);
    setGeneratedPost(null);
  };

  // const handleGeneratePost = async () => {
  //   if (!selectedNews) return;

  //   setIsGenerating(true);
  //   await new Promise((resolve) => setTimeout(resolve, 2500));

  //   setGeneratedPost(
  //     mockGeneratedPosts[selectedNews as keyof typeof mockGeneratedPosts]
  //   );
  //   setIsGenerating(false);
  // };

  const handleGeneratePost = async () => {
    if (!selectedNews) return;

    setIsGenerating(true);

    const newsItem = combinedNews.find((item) => item.id === selectedNews);

    if (!newsItem) {
      console.error("News item not found.");
      return;
    }

    const payload = {
      title: newsItem.title,
      summary: newsItem.summary,
      url: newsItem.url,
    };

    try {
      const result = await generatePost(payload).unwrap();
      setGeneratedPost(result);
    } catch (error) {
      console.error(error);
    } finally {
      setIsGenerating(false);
    }
  };

  const selectedNewsItem = filteredNews.find(
    (news) => news.id === selectedNews
  );

  if (isLoading) return <div>Loading news...</div>;
  if (error) return <div>Error loading news.</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-50/30">
      {/* Tim Hortons Branded Header */}
      <header className="border-b border-white/20 bg-white/90 backdrop-blur-xl sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-2xl flex items-center justify-center shadow-lg">
                  <Sparkles className="w-7 h-7 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white flex items-center justify-center">
                  <Heart className="w-2 h-2 text-white fill-white" />
                </div>
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-red-600 to-red-700 bg-clip-text text-transparent">
                  IBrand
                </h1>
                <p className="text-sm text-slate-600 font-medium">
                  Tim Hortons Social Intelligence
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Badge
                variant="secondary"
                className="bg-red-100 text-red-700 border-red-200 px-3 py-1"
              >
                <MapPin className="w-3 h-3 mr-1" />
                🇨🇦 Canada
              </Badge>
              <Badge
                variant="secondary"
                className="bg-emerald-100 text-emerald-700 border-emerald-200 px-3 py-1"
              >
                <Zap className="w-3 h-3 mr-1" />
                AI Active
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid xl:grid-cols-5 gap-8">
          {/* News Section - Takes up 3 columns */}
          <div className="xl:col-span-3 space-y-6">
            {/* Modern Header with Stats */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-slate-900">
                    Trending News
                  </h2>
                  <p className="text-sm text-slate-600">
                    {filteredNews.length} articles • Updated 2 min ago
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Badge className="bg-red-500/10 text-red-600 border-red-200">
                  <div className="w-2 h-2 bg-red-500 rounded-full mr-2 animate-pulse"></div>
                  Live
                </Badge>
              </div>
            </div>

            {/* Modern Search and Filters */}
            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
                    <Input
                      placeholder="Search news, topics, or tags..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10 border-slate-200 focus:border-red-500 focus:ring-red-500/20"
                    />
                  </div>
                  <Select
                    value={selectedCategory}
                    onValueChange={setSelectedCategory}
                  >
                    <SelectTrigger className="border-slate-200 focus:border-red-500 focus:ring-red-500/20">
                      <Filter className="w-4 h-4 mr-2 text-slate-400" />
                      <SelectValue placeholder="Category" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((category) => (
                        <SelectItem key={category} value={category}>
                          {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Select value={sortBy} onValueChange={setSortBy}>
                    <SelectTrigger className="border-slate-200 focus:border-red-500 focus:ring-red-500/20">
                      <BarChart3 className="w-4 h-4 mr-2 text-slate-400" />
                      <SelectValue placeholder="Sort by" />
                    </SelectTrigger>
                    <SelectContent>
                      {sortOptions.map((option) => (
                        <SelectItem key={option} value={option}>
                          {option}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            {/* News Grid */}
            <div className="space-y-4">
              {filteredNews.map((news) => (
                <Card
                  key={news.id}
                  className={`group cursor-pointer transition-all duration-300 border-0 shadow-md hover:shadow-xl bg-white/80 backdrop-blur-sm ${
                    selectedNews === news.id
                      ? "ring-2 ring-red-500 shadow-xl bg-red-50/50"
                      : "hover:shadow-lg hover:bg-white/90"
                  }`}
                  onClick={() => handleSelectNews(news.id)}
                >
                  <CardContent className="p-6">
                    <div className="flex space-x-5">
                      <div className="relative flex-shrink-0">
                        <img
                          src={news.image || "/placeholder.svg"}
                          alt={news.title}
                          className="w-32 h-24 rounded-xl object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                        {news.trending && (
                          <div className="absolute -top-2 -right-2 bg-gradient-to-r from-orange-500 to-red-500 text-white text-xs px-2 py-1 rounded-full font-medium shadow-lg">
                            🔥 Hot
                          </div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-3">
                          <Badge
                            variant="outline"
                            className="text-xs font-medium border-slate-300"
                          >
                            {news.category}
                          </Badge>
                          <div className="flex items-center space-x-1 text-xs text-slate-500">
                            <Calendar className="w-3 h-3" />
                            <span>
                              {new Date(news.publishedAt).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                        <h3 className="font-bold text-slate-900 text-lg leading-tight mb-3 group-hover:text-red-600 transition-colors">
                          {news.title}
                        </h3>
                        <p className="text-slate-600 text-sm leading-relaxed mb-4 line-clamp-2">
                          {news.summary}
                        </p>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4 text-xs text-slate-500">
                            <span className="font-medium">{news.source}</span>
                            <div className="flex items-center space-x-1">
                              <Clock className="w-3 h-3" />
                              <span>{news.readTime}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Eye className="w-3 h-3" />
                              <span>{news.views}</span>
                            </div>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {news.tags.slice(0, 2).map((tag, index) => (
                              <Badge
                                key={index}
                                variant="secondary"
                                className="text-xs bg-slate-100 text-slate-600"
                              >
                                #{tag}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* AI Generation Section - Takes up 2 columns */}
          <div className="xl:col-span-2 space-y-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-red-500 to-red-600 rounded-xl">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-slate-900">
                  Tim Hortons AI Studio
                </h2>
                <p className="text-sm text-slate-600">
                  Generate engaging Canadian content
                </p>
              </div>
            </div>

            {!selectedNews ? (
              <Card className="border-0 shadow-lg bg-gradient-to-br from-red-50 to-red-100/50 backdrop-blur-sm">
                <CardContent className="p-8 text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-red-200 to-red-300 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <TrendingUp className="w-10 h-10 text-red-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">
                    Select News to Begin
                  </h3>
                  <p className="text-slate-600 leading-relaxed">
                    Choose any trending news article to generate Tim
                    Hortons-branded social media content that builds Canadian
                    pride and community engagement
                  </p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-6">
                {/* Selected News Preview */}
                <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                  <CardHeader className="pb-4">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg font-bold text-slate-900">
                        Selected Article
                      </CardTitle>
                      <Button
                        onClick={handleGeneratePost}
                        disabled={isGenerating}
                        className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 shadow-lg"
                      >
                        {isGenerating ? (
                          <>
                            <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                            Generating...
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-4 h-4 mr-2" />
                            Generate Tim Hortons Post
                          </>
                        )}
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex space-x-4">
                      <img
                        src={selectedNewsItem?.image || "/placeholder.svg"}
                        alt={selectedNewsItem?.title}
                        className="w-20 h-16 rounded-lg object-cover"
                      />
                      <div className="flex-1">
                        <h4 className="font-bold text-slate-900 mb-2 leading-tight">
                          {selectedNewsItem?.title}
                        </h4>
                        <p className="text-sm text-slate-600 leading-relaxed">
                          {selectedNewsItem?.summary}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Generated Post */}
                {generatedPost && (
                  <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div>
                          <CardTitle className="text-lg font-bold text-slate-900">
                            Tim Hortons Content
                          </CardTitle>
                          <CardDescription className="text-slate-600">
                            Optimized for {generatedPost.platform} • Ready to
                            publish
                          </CardDescription>
                        </div>
                        <div className="flex space-x-2">
                          <Button
                            variant="outline"
                            size="sm"
                            className="border-slate-300"
                          >
                            <Share2 className="w-4 h-4 mr-2" />
                            Share
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            className="border-slate-300"
                          >
                            <Download className="w-4 h-4 mr-2" />
                            Export
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      {/* Generated Image */}
                      <div className="relative">
                        <img
                          src={generatedPost.image || "/placeholder.svg"}
                          alt="Generated post image"
                          className="w-full h-64 object-cover rounded-xl"
                        />
                        <Badge className="absolute top-3 right-3 bg-red-600 text-white shadow-lg">
                          <Sparkles className="w-3 h-3 mr-1" />
                          Tim Hortons AI
                        </Badge>
                      </div>

                      {/* Post Content */}
                      <div className="bg-gradient-to-br from-red-50 to-red-100/30 rounded-xl p-6 border border-red-200">
                        <div className="flex items-center space-x-3 mb-4">
                          <Avatar className="w-10 h-10 ring-2 ring-red-200">
                            <AvatarImage src="/placeholder.svg?height=40&width=40" />
                            <AvatarFallback className="bg-gradient-to-br from-red-600 to-red-700 text-white font-bold">
                              TH
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="font-bold text-slate-900">
                              Tim Hortons
                            </p>
                            <p className="text-xs text-slate-500">
                              Just now • {generatedPost.platform}
                            </p>
                          </div>
                        </div>
                        <p className="text-sm whitespace-pre-line mb-4 leading-relaxed text-slate-800">
                          {generatedPost.content}
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {generatedPost.hashtags.map(
                            (tag: string, index: number) => (
                              <Badge
                                key={index}
                                variant="secondary"
                                className="text-xs bg-red-100 text-red-700 border-red-200"
                              >
                                {tag}
                              </Badge>
                            )
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
      <AiChatWidget />
    </div>
  );
}

import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

export interface NewsItem {
  _id: string
  url: string
  source: string
  title: string
  author: string
  published_at: string
  summary: string
  content: string
  seeded_at: string
  bias: {
    label: string
    score: number
  }
  sentiment: {
    label: string
    score: number
  }
  tags: string[]
  enriched_at: string
}

export const newsApi = createApi({
  reducerPath: "newsApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://0.0.0.0:8000/",
  }),
  endpoints: (builder) => ({
    getNews: builder.query<NewsItem[], void>({
      query: () => "news",
    }),
  }),
})

export const { useGetNewsQuery } = newsApi

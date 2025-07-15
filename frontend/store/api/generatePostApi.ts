import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export interface GeneratePostRequest {
  title: string;
  summary: string;
  url: string;
}

export interface GeneratePostResponse {
  platform: string;
  content: string;
  hashtags: string[];
  image: string;
  created_at: string | null;
}

export const generatePostApi = createApi({
  reducerPath: "generatePostApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://0.0.0.0:8000/",
    prepareHeaders: (headers) => {
      // If you want to add auth tokens or custom headers, do here
      // headers.set("Authorization", `Bearer ${token}`);
      return headers;
    },
  }),
  tagTypes: ["GeneratedPost"], // helpful for cache invalidation if you extend in future
  endpoints: (builder) => ({
    generatePost: builder.mutation<
      GeneratePostResponse,
      GeneratePostRequest
    >({
      query: (body) => ({
        url: "generate-post",
        method: "POST",
        body,
        // Optional: you can add headers or params here if needed
      }),
      // Optional: you can add invalidatesTags or providesTags here if you want cache control
      // invalidatesTags: ["GeneratedPost"],
    }),
  }),
});

export const { useGeneratePostMutation } = generatePostApi;

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
  }),
  endpoints: (builder) => ({
    generatePost: builder.mutation<
      GeneratePostResponse,
      GeneratePostRequest
    >({
      query: (body) => ({
        url: "generate-post",
        method: "POST",
        body,
      }),
    }),
  }),
});

export const { useGeneratePostMutation } = generatePostApi;

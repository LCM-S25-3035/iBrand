import { configureStore } from "@reduxjs/toolkit"
import { newsApi } from "./api/newsApi"
import { generatePostApi } from "./api/generatePostApi";


export const store = configureStore({
  reducer: {
    [newsApi.reducerPath]: newsApi.reducer,
    [generatePostApi.reducerPath]: generatePostApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(newsApi.middleware,generatePostApi.middleware
    ),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

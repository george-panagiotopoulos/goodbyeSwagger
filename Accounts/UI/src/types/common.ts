export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}

export interface ApiResponse<T> {
  data: T;
  _links?: Record<string, Link>;
}

export interface Link {
  href: string;
  method?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
  _links?: Record<string, Link>;
}

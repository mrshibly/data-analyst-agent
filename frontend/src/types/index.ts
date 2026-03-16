export interface ColumnInfo {
  name: string;
  dtype: string;
  non_null_count: number;
  null_count: number;
}

export interface UploadResponse {
  file_id: string;
  filename: string;
  row_count: number;
  column_count: number;
  file_size: number;
  columns: ColumnInfo[];
  preview: any[];
}

export interface ChartInfo {
  title: string;
  url?: string;
  plotly_data?: any;
  chart_type?: string;
  is_interactive: boolean;
}

export interface StatisticsInfo {
  row_count: number;
  column_count: number;
  numeric_columns: string[];
  categorical_columns: string[];
}

export interface AnalysisResponse {
  summary: string;
  insights: string[];
  charts: ChartInfo[];
  statistics: StatisticsInfo;
  tool_used?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

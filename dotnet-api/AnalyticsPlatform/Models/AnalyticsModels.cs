namespace AnalyticsPlatform.Models
{
    public class ValidRecord
    {
        public int Id { get; set; }
        public string? RecordId { get; set; }
        public string? CustomerId { get; set; }
        public string? ProductId { get; set; }
        public decimal? Quantity { get; set; }
        public decimal? UnitPrice { get; set; }
        public decimal? TotalAmount { get; set; }
        public DateTime? TransactionDate { get; set; }
        public string? Region { get; set; }
        public string? Category { get; set; }
        public DateTime? ProcessedAt { get; set; }
    }

    public class InvalidRecord
    {
        public int Id { get; set; }
        public string? RecordId { get; set; }
        public string? RawData { get; set; }
        public string[]? ValidationErrors { get; set; }
        public string? SourceFile { get; set; }
        public DateTime? FlaggedAt { get; set; }
    }

    public class Anomaly
    {
        public int Id { get; set; }
        public string? RecordId { get; set; }
        public string? CustomerId { get; set; }
        public decimal? TotalAmount { get; set; }
        public decimal? AnomalyScore { get; set; }
        public string? AnomalyType { get; set; }
        public string? DetectionMethod { get; set; }
        public DateTime? DetectedAt { get; set; }
    }

    public class AiInsight
    {
        public int Id { get; set; }
        public string? InsightType { get; set; }
        public string? InsightText { get; set; }
        public string? ModelUsed { get; set; }
        public DateTime? GeneratedAt { get; set; }
    }

    public class SummaryMetric
    {
        public int Id { get; set; }
        public DateTime? MetricDate { get; set; }
        public int? TotalRecords { get; set; }
        public int? ValidRecords { get; set; }
        public int? InvalidRecords { get; set; }
        public int? AnomalyCount { get; set; }
        public decimal? TotalRevenue { get; set; }
        public decimal? AvgOrderValue { get; set; }
        public string? TopRegion { get; set; }
        public string? TopCategory { get; set; }
        public DateTime? ComputedAt { get; set; }
    }
}
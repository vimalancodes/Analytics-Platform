using Microsoft.EntityFrameworkCore;
using AnalyticsPlatform.Models;

namespace AnalyticsPlatform.Data
{
    public class AnalyticsDbContext : DbContext
    {
        public AnalyticsDbContext(DbContextOptions<AnalyticsDbContext> options) : base(options) { }

        public DbSet<ValidRecord> ValidRecords { get; set; }
        public DbSet<InvalidRecord> InvalidRecords { get; set; }
        public DbSet<Anomaly> Anomalies { get; set; }
        public DbSet<AiInsight> AiInsights { get; set; }
        public DbSet<SummaryMetric> SummaryMetrics { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<ValidRecord>().ToTable("valid_records");
            modelBuilder.Entity<ValidRecord>().Property(e => e.Id).HasColumnName("id");
            modelBuilder.Entity<ValidRecord>().Property(e => e.RecordId).HasColumnName("record_id");
            modelBuilder.Entity<ValidRecord>().Property(e => e.CustomerId).HasColumnName("customer_id");
            modelBuilder.Entity<ValidRecord>().Property(e => e.ProductId).HasColumnName("product_id");
            modelBuilder.Entity<ValidRecord>().Property(e => e.Quantity).HasColumnName("quantity");
            modelBuilder.Entity<ValidRecord>().Property(e => e.UnitPrice).HasColumnName("unit_price");
            modelBuilder.Entity<ValidRecord>().Property(e => e.TotalAmount).HasColumnName("total_amount");
            modelBuilder.Entity<ValidRecord>().Property(e => e.TransactionDate).HasColumnName("transaction_date");
            modelBuilder.Entity<ValidRecord>().Property(e => e.Region).HasColumnName("region");
            modelBuilder.Entity<ValidRecord>().Property(e => e.Category).HasColumnName("category");
            modelBuilder.Entity<ValidRecord>().Property(e => e.ProcessedAt).HasColumnName("processed_at");

            modelBuilder.Entity<InvalidRecord>().ToTable("invalid_records");
            modelBuilder.Entity<InvalidRecord>().Property(e => e.Id).HasColumnName("id");
            modelBuilder.Entity<InvalidRecord>().Property(e => e.RecordId).HasColumnName("record_id");
            modelBuilder.Entity<InvalidRecord>().Property(e => e.RawData).HasColumnName("raw_data");
            modelBuilder.Entity<InvalidRecord>().Property(e => e.ValidationErrors).HasColumnName("validation_errors");
            modelBuilder.Entity<InvalidRecord>().Property(e => e.SourceFile).HasColumnName("source_file");
            modelBuilder.Entity<InvalidRecord>().Property(e => e.FlaggedAt).HasColumnName("flagged_at");

            modelBuilder.Entity<Anomaly>().ToTable("anomalies");
            modelBuilder.Entity<Anomaly>().Property(e => e.Id).HasColumnName("id");
            modelBuilder.Entity<Anomaly>().Property(e => e.RecordId).HasColumnName("record_id");
            modelBuilder.Entity<Anomaly>().Property(e => e.CustomerId).HasColumnName("customer_id");
            modelBuilder.Entity<Anomaly>().Property(e => e.TotalAmount).HasColumnName("total_amount");
            modelBuilder.Entity<Anomaly>().Property(e => e.AnomalyScore).HasColumnName("anomaly_score");
            modelBuilder.Entity<Anomaly>().Property(e => e.AnomalyType).HasColumnName("anomaly_type");
            modelBuilder.Entity<Anomaly>().Property(e => e.DetectionMethod).HasColumnName("detection_method");
            modelBuilder.Entity<Anomaly>().Property(e => e.DetectedAt).HasColumnName("detected_at");

            modelBuilder.Entity<AiInsight>().ToTable("ai_insights");
            modelBuilder.Entity<AiInsight>().Property(e => e.Id).HasColumnName("id");
            modelBuilder.Entity<AiInsight>().Property(e => e.InsightType).HasColumnName("insight_type");
            modelBuilder.Entity<AiInsight>().Property(e => e.InsightText).HasColumnName("insight_text");
            modelBuilder.Entity<AiInsight>().Property(e => e.ModelUsed).HasColumnName("model_used");
            modelBuilder.Entity<AiInsight>().Property(e => e.GeneratedAt).HasColumnName("generated_at");

            modelBuilder.Entity<SummaryMetric>().ToTable("summary_metrics");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.Id).HasColumnName("id");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.MetricDate).HasColumnName("metric_date");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.TotalRecords).HasColumnName("total_records");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.ValidRecords).HasColumnName("valid_records");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.InvalidRecords).HasColumnName("invalid_records");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.AnomalyCount).HasColumnName("anomaly_count");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.TotalRevenue).HasColumnName("total_revenue");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.AvgOrderValue).HasColumnName("avg_order_value");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.TopRegion).HasColumnName("top_region");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.TopCategory).HasColumnName("top_category");
            modelBuilder.Entity<SummaryMetric>().Property(e => e.ComputedAt).HasColumnName("computed_at");
        }
    }
}
# Load required package and import dataset
library(readr)
Auto <- read_csv("/Users/julianjaramillo/Desktop/Data_analytics/Auto.csv")

# Inspect dataset structure
cat("Class: ", class(Auto), "\n")
cat("Type: ", typeof(Auto), "\n")

# Utility function to return dataset dimensions
get_dimensions <- function(df) {
  return(dim(df))
}

# Display dimensions before data cleaning
cat("Original Dimensions: ", get_dimensions(Auto), "\n")

# Data cleaning: replace "?" with NA and remove missing values
Auto[Auto == "?"] <- NA
Auto <- na.omit(Auto)

# Display dimensions after cleaning
cat("Cleaned Dimensions: ", get_dimensions(Auto), "\n")

# List column names
print(names(Auto))

# Visualization: Cylinders vs MPG (raw numeric form)
plot(Auto$cylinders, Auto$mpg,
     xlab = "Cylinders",
     ylab = "MPG",
     main = "Cylinders by MPG (Numeric)",
     col = "green", pch = 16)

# Convert cylinders column to factor for categorical analysis
Auto$cylinders <- as.factor(Auto$cylinders)

# Visualization: Cylinders vs MPG (factor form)
plot(Auto$cylinders, Auto$mpg,
     xlab = "Cylinders",
     ylab = "MPG",
     main = "Cylinders by MPG (Factor)",
     col = "green")

# Visualization: Histogram of MPG
hist(Auto$mpg, breaks = 10,
     xlab = "MPG",
     main = "Distribution of MPG",
     border = "black", col = "green")

# Select relevant numeric fields for correlation analysis
auto_fields <- Auto[, c("mpg", "displacement", "horsepower", "weight", "acceleration")]
auto_fields <- auto_fields[, sapply(auto_fields, is.numeric)]

# Scatterplot matrix to visualize relationships
pairs(auto_fields,
      main = "Scatterplot Matrix of Key Variables",
      col = "blue", pch = 16, cex = 0.7)

# Summary statistics for entire dataset
summary(Auto)

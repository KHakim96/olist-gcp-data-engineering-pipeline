# Phase 00 – Project Planning

## Objective

The objective of this phase is to define the overall project architecture, technology stack, development roadmap, and project structure before implementation begins.

This project aims to simulate a real-world cloud data engineering platform by ingesting data from multiple sources into Google Cloud Platform, transforming the data into analytics-ready models, and serving business intelligence dashboards.

---

# Project Information

## Project Name

olist-gcp-data-engineering-pipeline

## Project Type

Cloud Data Engineering Project

## Project Goal

Build an end-to-end cloud-native data engineering pipeline capable of:

- Ingesting transactional data from CSV files
- Ingesting external weather data from a REST API
- Storing raw data in Google Cloud Storage
- Loading raw datasets into Google BigQuery
- Transforming data using dbt
- Building analytics-ready data marts
- Visualising insights using Power BI
- Orchestrating the complete workflow using Apache Airflow running on Google Compute Engine

---

# Technology Stack

## Programming

- Python

## Cloud Platform

- Google Cloud Platform (GCP)

## Cloud Services

- Compute Engine
- Google Cloud Storage
- BigQuery
- IAM
- Service Accounts

## Data Engineering

- Apache Airflow
- Docker
- Docker Compose
- dbt

## Data Warehouse

- Google BigQuery

## Data Visualisation

- Power BI

## Version Control

- Git
- GitHub

---

# Data Sources

## Internal Data Source

Olist E-Commerce Dataset

Tables

- Customers
- Orders
- Order Items
- Products
- Sellers
- Payments
- Reviews
- Geolocation
- Category Translation

## External Data Source

Weather API

Purpose

- Demonstrate API ingestion
- Simulate integration with external business systems
- Store raw API responses in Google Cloud Storage
- Load weather data into BigQuery

---

# Project Architecture

                              Google Cloud Platform

                      Compute Engine Virtual Machine
                                   │
                          Docker + Docker Compose
                                   │
                            Apache Airflow
                                   │
               ┌───────────────────┴───────────────────┐
               ▼                                       ▼
     Upload Olist CSV Files                   Fetch Weather API
            to Google Cloud Storage           Store JSON in GCS
                                   │
                                   ▼
                           BigQuery Raw Dataset
                                   │
                                   ▼
                          dbt Transformations
                                   │
                                   ▼
                         Analytics Data Mart
                                   │
                                   ▼
                             Power BI Dashboard

---

# Development Phases

Phase 00
Project Planning

Phase 01
Google Cloud Platform Setup

Phase 02
Compute Engine & Airflow

Phase 03
Google Cloud Storage

Phase 04
BigQuery Raw Layer

Phase 05
Airflow Orchestration

Phase 06
dbt Transformations

Phase 07
Power BI Dashboard

Phase 08
Testing & Data Quality

Phase 09
Documentation & Deployment

---

# Folder Structure

olist-gcp-data-engineering-pipeline/

├── config/
├── dags/
├── dashboard/
├── data/
├── dbt_olist/
├── docs/
├── notes/
├── scripts/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
└── .gitignore

---

# Deliverables

Completed

- Project structure
- Git repository initialization
- Documentation structure
- Development roadmap
- Technology selection
- Architecture design

---

# Status

Completed
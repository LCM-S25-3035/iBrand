Milestone 3 Presentation: HAS-GPU

I am presenting the following research paper as part of Milestone 3:

Title:
HAS-GPU: Efficient Hybrid Auto-scaling with Fine-grained GPU Allocation for SLO-aware Serverless Inferences

Abstract:
Serverless Computing (FaaS) has become a popular paradigm for deep learning inference due to the ease of deployment and pay-per-use benefits. However, current serverless inference platforms encounter the coarse-grained and static GPU resource allocation problems during scaling, which leads to high costs and Service Level Objective (SLO) violations in fluctuating workloads. Meanwhile, current platforms only support horizontal scaling for GPU inferences, thus the cold start problem further exacerbates the problems.

In this paper, the authors propose HAS-GPU, an efficient Hybrid Auto-scaling Serverless architecture with fine-grained GPU allocation for deep learning inferences. HAS-GPU introduces an agile scheduler capable of allocating GPU Streaming Multiprocessor (SM) partitions and time quotas with arbitrary granularity, enabling significant vertical quota scalability at runtime. 

To handle the performance uncertainty introduced by massive fine-grained resource configuration spaces, the paper proposes the Resource-aware Performance Predictor (RaPP). Additionally, an adaptive hybrid auto-scaling algorithm is presented, combining both horizontal and vertical scaling to ensure inference SLOs while minimizing GPU costs.

Experimental results demonstrate that, compared to mainstream serverless inference platforms, HAS-GPU reduces function costs by an average of **10.8x** with improved SLO guarantees. Compared to the state-of-the-art spatio-temporal GPU sharing serverless framework, HAS-GPU achieves **4.8x** lower SLO violations and **1.72x** cost reduction on average.

Details:
- **Year**: 2 May 2025  
- **Conference/Journal**: Euro-Par  
- **Authors**: Jianfeng Gu, Puxuan Wang, Isaac David Núñez Araya, Kai Huang, Michael Gerndt  
- **Project Link**: https://www.ce.cit.tum.de/caps/aktuelles/news-single-view/article/has-gpu-efficient-hybrid-auto-scaling-with-fine-grained-gpu-allocation-for-slo-aware-serverless-inferences-got-accepted-at-euro-par-2025/




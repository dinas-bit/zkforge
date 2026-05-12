/*
 * ZKForge NTT HIP Kernel
 * GPU-parallel Number Theoretic Transform
 */
#include <hip/hip_runtime.h>
#include <stdint.h>

__global__ void ntt_butterfly(
    uint64_t *data,
    const uint64_t *twiddle,
    uint32_t n,
    uint32_t half_len,
    uint64_t modulus
) {
    uint32_t idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n / 2) return;

    uint32_t group = idx / half_len;
    uint32_t pos = idx % half_len;
    uint32_t i = group * half_len * 2 + pos;

    uint64_t u = data[i];
    uint64_t v = data[i + half_len];
    uint64_t w = twiddle[pos * (n / (2 * half_len))];

    // Modular multiplication: v * w mod p
    __uint128_t product = (__uint128_t)v * w;
    uint64_t vw = product % modulus;

    data[i] = (u + vw) % modulus;
    data[i + half_len] = (u + modulus - vw % modulus) % modulus;
}

__global__ void msm_bucket_accumulate(
    const uint64_t *scalars,
    const uint64_t *points_x,
    const uint64_t *points_y,
    uint64_t *buckets_x,
    uint64_t *buckets_y,
    uint32_t num_points,
    uint32_t window_bits,
    uint32_t window_idx,
    uint64_t modulus
) {
    uint32_t idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= num_points) return;

    uint32_t bucket = (scalars[idx] >> (window_idx * window_bits)) & ((1 << window_bits) - 1);
    if (bucket == 0) return;

    // Atomic add to bucket (point addition)
    atomicAdd(&buckets_x[bucket], points_x[idx]);
    atomicAdd(&buckets_y[bucket], points_y[idx]);
}

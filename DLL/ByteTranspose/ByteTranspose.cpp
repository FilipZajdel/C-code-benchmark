#include "stdafx.h"
#include "ByteTranspose.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

void WINAPI Deinterleve_16Bytes_to_2x8Bytes(BYTE *pbSource, DWORD count)
{
    BYTE lsb[8], msb[8];

    for (DWORD i = 0; i < count; i++)
    {
        for (char j = 0; j < 8; j++)
        {
            lsb[j] = pbSource[j * 2];
            msb[j] = pbSource[(j * 2) + 1];
        }
        for (char j = 0; j < 8; j++)
        {
            pbSource[j] = lsb[j];
            pbSource[j + 8] = msb[j];
        }
        pbSource += 16;
    }
}

inline void WINAPI TransposeByte8x8(BYTE *source, BYTE *destination)
{
    destination[7] = (((source[0] & (1 << 7)) >> 0) |
                      ((source[1] & (1 << 7)) >> 1) |
                      ((source[2] & (1 << 7)) >> 2) |
                      ((source[3] & (1 << 7)) >> 3) |
                      ((source[4] & (1 << 7)) >> 4) |
                      ((source[5] & (1 << 7)) >> 5) |
                      ((source[6] & (1 << 7)) >> 6) |
                      ((source[7] & (1 << 7)) >> 7));

    destination[6] = (((source[0] & (1 << 6)) << 1) |
                      ((source[1] & (1 << 6)) >> 0) |
                      ((source[2] & (1 << 6)) >> 1) |
                      ((source[3] & (1 << 6)) >> 2) |
                      ((source[4] & (1 << 6)) >> 3) |
                      ((source[5] & (1 << 6)) >> 4) |
                      ((source[6] & (1 << 6)) >> 5) |
                      ((source[7] & (1 << 6)) >> 6));

    destination[5] = (((source[0] & (1 << 5)) << 2) |
                      ((source[1] & (1 << 5)) << 1) |
                      ((source[2] & (1 << 5)) >> 0) |
                      ((source[3] & (1 << 5)) >> 1) |
                      ((source[4] & (1 << 5)) >> 2) |
                      ((source[5] & (1 << 5)) >> 3) |
                      ((source[6] & (1 << 5)) >> 4) |
                      ((source[7] & (1 << 5)) >> 5));

    destination[4] = (((source[0] & (1 << 4)) << 3) |
                      ((source[1] & (1 << 4)) << 2) |
                      ((source[2] & (1 << 4)) << 1) |
                      ((source[3] & (1 << 4)) >> 0) |
                      ((source[4] & (1 << 4)) >> 1) |
                      ((source[5] & (1 << 4)) >> 2) |
                      ((source[6] & (1 << 4)) >> 3) |
                      ((source[7] & (1 << 4)) >> 4));

    destination[3] = (((source[0] & (1 << 3)) << 4) |
                      ((source[1] & (1 << 3)) << 3) |
                      ((source[2] & (1 << 3)) << 2) |
                      ((source[3] & (1 << 3)) << 1) |
                      ((source[4] & (1 << 3)) >> 0) |
                      ((source[5] & (1 << 3)) >> 1) |
                      ((source[6] & (1 << 3)) >> 2) |
                      ((source[7] & (1 << 3)) >> 3));

    destination[2] = (((source[0] & (1 << 2)) << 5) |
                      ((source[1] & (1 << 2)) << 4) |
                      ((source[2] & (1 << 2)) << 3) |
                      ((source[3] & (1 << 2)) << 2) |
                      ((source[4] & (1 << 2)) << 1) |
                      ((source[5] & (1 << 2)) >> 0) |
                      ((source[6] & (1 << 2)) >> 1) |
                      ((source[7] & (1 << 2)) >> 2));

    destination[1] = (((source[0] & (1 << 1)) << 6) |
                      ((source[1] & (1 << 1)) << 5) |
                      ((source[2] & (1 << 1)) << 4) |
                      ((source[3] & (1 << 1)) << 3) |
                      ((source[4] & (1 << 1)) << 2) |
                      ((source[5] & (1 << 1)) << 1) |
                      ((source[6] & (1 << 1)) >> 0) |
                      ((source[7] & (1 << 1)) >> 1));

    destination[0] = (((source[0] & (1 << 0)) << 7) |
                      ((source[1] & (1 << 0)) << 6) |
                      ((source[2] & (1 << 0)) << 5) |
                      ((source[3] & (1 << 0)) << 4) |
                      ((source[4] & (1 << 0)) << 3) |
                      ((source[5] & (1 << 0)) << 2) |
                      ((source[6] & (1 << 0)) << 1) |
                      ((source[7] & (1 << 0)) >> 0));
}

inline BYTE_TRANSPOSE_API void WINAPI TransposeWords16x16(WORD *source, WORD *destination)
{
    destination[15] = (((source[0] & (1 << 15)) >> 0) |
                       ((source[1] & (1 << 15)) >> 1) |
                       ((source[2] & (1 << 15)) >> 2) |
                       ((source[3] & (1 << 15)) >> 3) |
                       ((source[4] & (1 << 15)) >> 4) |
                       ((source[5] & (1 << 15)) >> 5) |
                       ((source[6] & (1 << 15)) >> 6) |
                       ((source[7] & (1 << 15)) >> 7) |
                       ((source[8] & (1 << 15)) >> 8) |
                       ((source[9] & (1 << 15)) >> 9) |
                       ((source[10] & (1 << 15)) >> 10) |
                       ((source[11] & (1 << 15)) >> 11) |
                       ((source[12] & (1 << 15)) >> 12) |
                       ((source[13] & (1 << 15)) >> 13) |
                       ((source[14] & (1 << 15)) >> 14) |
                       ((source[15] & (1 << 15)) >> 15));

    destination[14] = (((source[0] & (1 << 14)) << 1) |
                       ((source[1] & (1 << 14)) >> 0) |
                       ((source[2] & (1 << 14)) >> 1) |
                       ((source[3] & (1 << 14)) >> 2) |
                       ((source[4] & (1 << 14)) >> 3) |
                       ((source[5] & (1 << 14)) >> 4) |
                       ((source[6] & (1 << 14)) >> 5) |
                       ((source[7] & (1 << 14)) >> 6) |
                       ((source[8] & (1 << 14)) >> 7) |
                       ((source[9] & (1 << 14)) >> 8) |
                       ((source[10] & (1 << 14)) >> 9) |
                       ((source[11] & (1 << 14)) >> 10) |
                       ((source[12] & (1 << 14)) >> 11) |
                       ((source[13] & (1 << 14)) >> 12) |
                       ((source[14] & (1 << 14)) >> 13) |
                       ((source[15] & (1 << 14)) >> 14));

    destination[13] = (((source[0] & (1 << 13)) << 2) |
                       ((source[1] & (1 << 13)) << 1) |
                       ((source[2] & (1 << 13)) >> 0) |
                       ((source[3] & (1 << 13)) >> 1) |
                       ((source[4] & (1 << 13)) >> 2) |
                       ((source[5] & (1 << 13)) >> 3) |
                       ((source[6] & (1 << 13)) >> 4) |
                       ((source[7] & (1 << 13)) >> 5) |
                       ((source[8] & (1 << 13)) >> 6) |
                       ((source[9] & (1 << 13)) >> 7) |
                       ((source[10] & (1 << 13)) >> 8) |
                       ((source[11] & (1 << 13)) >> 9) |
                       ((source[12] & (1 << 13)) >> 10) |
                       ((source[13] & (1 << 13)) >> 11) |
                       ((source[14] & (1 << 13)) >> 12) |
                       ((source[15] & (1 << 13)) >> 13));

    destination[12] = (((source[0] & (1 << 12)) << 3) |
                       ((source[1] & (1 << 12)) << 2) |
                       ((source[2] & (1 << 12)) << 1) |
                       ((source[3] & (1 << 12)) >> 0) |
                       ((source[4] & (1 << 12)) >> 1) |
                       ((source[5] & (1 << 12)) >> 2) |
                       ((source[6] & (1 << 12)) >> 3) |
                       ((source[7] & (1 << 12)) >> 4) |
                       ((source[8] & (1 << 12)) >> 5) |
                       ((source[9] & (1 << 12)) >> 6) |
                       ((source[10] & (1 << 12)) >> 7) |
                       ((source[11] & (1 << 12)) >> 8) |
                       ((source[12] & (1 << 12)) >> 9) |
                       ((source[13] & (1 << 12)) >> 10) |
                       ((source[14] & (1 << 12)) >> 11) |
                       ((source[15] & (1 << 12)) >> 12));

    destination[11] = (((source[0] & (1 << 11)) << 4) |
                       ((source[1] & (1 << 11)) << 3) |
                       ((source[2] & (1 << 11)) << 2) |
                       ((source[3] & (1 << 11)) << 1) |
                       ((source[4] & (1 << 11)) >> 0) |
                       ((source[5] & (1 << 11)) >> 1) |
                       ((source[6] & (1 << 11)) >> 2) |
                       ((source[7] & (1 << 11)) >> 3) |
                       ((source[8] & (1 << 11)) >> 4) |
                       ((source[9] & (1 << 11)) >> 5) |
                       ((source[10] & (1 << 11)) >> 6) |
                       ((source[11] & (1 << 11)) >> 7) |
                       ((source[12] & (1 << 11)) >> 8) |
                       ((source[13] & (1 << 11)) >> 9) |
                       ((source[14] & (1 << 11)) >> 10) |
                       ((source[15] & (1 << 11)) >> 11));

    destination[10] = (((source[0] & (1 << 10)) << 5) |
                       ((source[1] & (1 << 10)) << 4) |
                       ((source[2] & (1 << 10)) << 3) |
                       ((source[3] & (1 << 10)) << 2) |
                       ((source[4] & (1 << 10)) << 1) |
                       ((source[5] & (1 << 10)) >> 0) |
                       ((source[6] & (1 << 10)) >> 1) |
                       ((source[7] & (1 << 10)) >> 2) |
                       ((source[8] & (1 << 10)) >> 3) |
                       ((source[9] & (1 << 10)) >> 4) |
                       ((source[10] & (1 << 10)) >> 5) |
                       ((source[11] & (1 << 10)) >> 6) |
                       ((source[12] & (1 << 10)) >> 7) |
                       ((source[13] & (1 << 10)) >> 8) |
                       ((source[14] & (1 << 10)) >> 9) |
                       ((source[15] & (1 << 10)) >> 10));

    destination[9] = (((source[0] & (1 << 9)) << 6) |
                       ((source[1] & (1 << 9)) << 5) |
                       ((source[2] & (1 << 9)) << 4) |
                       ((source[3] & (1 << 9)) << 3) |
                       ((source[4] & (1 << 9)) << 2) |
                       ((source[5] & (1 << 9)) << 1) |
                       ((source[6] & (1 << 9)) >> 0) |
                       ((source[7] & (1 << 9)) >> 1) |
                       ((source[8] & (1 << 9)) >> 2) |
                       ((source[9] & (1 << 9)) >> 3) |
                       ((source[10] & (1 << 9)) >> 4) |
                       ((source[11] & (1 << 9)) >> 5) |
                       ((source[12] & (1 << 9)) >> 6) |
                       ((source[13] & (1 << 9)) >> 7) |
                       ((source[14] & (1 << 9)) >> 8) |
                       ((source[15] & (1 << 9)) >> 9));

    destination[8] = (((source[0] & (1 << 8)) << 7) |
                       ((source[1] & (1 << 8)) << 6) |
                       ((source[2] & (1 << 8)) << 5) |
                       ((source[3] & (1 << 8)) << 4) |
                       ((source[4] & (1 << 8)) << 3) |
                       ((source[5] & (1 << 8)) << 2) |
                       ((source[6] & (1 << 8)) << 1) |
                       ((source[7] & (1 << 8)) >> 0) |
                       ((source[8] & (1 << 8)) >> 1) |
                       ((source[9] & (1 << 8)) >> 2) |
                       ((source[10] & (1 << 8)) >> 3) |
                       ((source[11] & (1 << 8)) >> 4) |
                       ((source[12] & (1 << 8)) >> 5) |
                       ((source[13] & (1 << 8)) >> 6) |
                       ((source[14] & (1 << 8)) >> 7) |
                       ((source[15] & (1 << 8)) >> 8));

    destination[7] = (((source[0] & (1 << 7)) << 8) |
                       ((source[1] & (1 << 7)) << 7) |
                       ((source[2] & (1 << 7)) << 6) |
                       ((source[3] & (1 << 7)) << 5) |
                       ((source[4] & (1 << 7)) << 4) |
                       ((source[5] & (1 << 7)) << 3) |
                       ((source[6] & (1 << 7)) << 2) |
                       ((source[7] & (1 << 7)) << 1) |
                       ((source[8] & (1 << 7)) >> 0) |
                       ((source[9] & (1 << 7)) >> 1) |
                       ((source[10] & (1 << 7)) >> 2) |
                       ((source[11] & (1 << 7)) >> 3) |
                       ((source[12] & (1 << 7)) >> 4) |
                       ((source[13] & (1 << 7)) >> 5) |
                       ((source[14] & (1 << 7)) >> 6) |
                       ((source[15] & (1 << 7)) >> 7));

    destination[6] = (((source[0] & (1 << 6)) << 9) |
                       ((source[1] & (1 << 6)) << 8) |
                       ((source[2] & (1 << 6)) << 7) |
                       ((source[3] & (1 << 6)) << 6) |
                       ((source[4] & (1 << 6)) << 5) |
                       ((source[5] & (1 << 6)) << 4) |
                       ((source[6] & (1 << 6)) << 3) |
                       ((source[7] & (1 << 6)) << 2) |
                       ((source[8] & (1 << 6)) << 1) |
                       ((source[9] & (1 << 6)) >> 0) |
                       ((source[10] & (1 << 6)) >> 1) |
                       ((source[11] & (1 << 6)) >> 2) |
                       ((source[12] & (1 << 6)) >> 3) |
                       ((source[13] & (1 << 6)) >> 4) |
                       ((source[14] & (1 << 6)) >> 5) |
                       ((source[15] & (1 << 6)) >> 6));

    destination[5] = (((source[0] & (1 << 5)) << 10) |
                       ((source[1] & (1 << 5)) << 9) |
                       ((source[2] & (1 << 5)) << 8) |
                       ((source[3] & (1 << 5)) << 7) |
                       ((source[4] & (1 << 5)) << 6) |
                       ((source[5] & (1 << 5)) << 5) |
                       ((source[6] & (1 << 5)) << 4) |
                       ((source[7] & (1 << 5)) << 3) |
                       ((source[8] & (1 << 5)) << 2) |
                       ((source[9] & (1 << 5)) << 1) |
                       ((source[10] & (1 << 5)) >> 0) |
                       ((source[11] & (1 << 5)) >> 1) |
                       ((source[12] & (1 << 5)) >> 2) |
                       ((source[13] & (1 << 5)) >> 3) |
                       ((source[14] & (1 << 5)) >> 4) |
                       ((source[15] & (1 << 5)) >> 5));

    destination[4] = (((source[0] & (1 << 4)) << 11) |
                       ((source[1] & (1 << 4)) << 10) |
                       ((source[2] & (1 << 4)) << 9) |
                       ((source[3] & (1 << 4)) << 8) |
                       ((source[4] & (1 << 4)) << 7) |
                       ((source[5] & (1 << 4)) << 6) |
                       ((source[6] & (1 << 4)) << 5) |
                       ((source[7] & (1 << 4)) << 4) |
                       ((source[8] & (1 << 4)) << 3) |
                       ((source[9] & (1 << 4)) << 2) |
                       ((source[10] & (1 << 4)) << 1) |
                       ((source[11] & (1 << 4)) >> 0) |
                       ((source[12] & (1 << 4)) >> 1) |
                       ((source[13] & (1 << 4)) >> 2) |
                       ((source[14] & (1 << 4)) >> 3) |
                       ((source[15] & (1 << 4)) >> 4));

    destination[3] = (((source[0] & (1 << 3)) << 12) |
                       ((source[1] & (1 << 3)) << 11) |
                       ((source[2] & (1 << 3)) << 10) |
                       ((source[3] & (1 << 3)) << 9) |
                       ((source[4] & (1 << 3)) << 8) |
                       ((source[5] & (1 << 3)) << 7) |
                       ((source[6] & (1 << 3)) << 6) |
                       ((source[7] & (1 << 3)) << 5) |
                       ((source[8] & (1 << 3)) << 4) |
                       ((source[9] & (1 << 3)) << 3) |
                       ((source[10] & (1 << 3)) << 2) |
                       ((source[11] & (1 << 3)) << 1) |
                       ((source[12] & (1 << 3)) >> 0) |
                       ((source[13] & (1 << 3)) >> 1) |
                       ((source[14] & (1 << 3)) >> 2) |
                       ((source[15] & (1 << 3)) >> 3));

    destination[2] = (((source[0] & (1 << 2)) << 13) |
                       ((source[1] & (1 << 2)) << 12) |
                       ((source[2] & (1 << 2)) << 11) |
                       ((source[3] & (1 << 2)) << 10) |
                       ((source[4] & (1 << 2)) << 9) |
                       ((source[5] & (1 << 2)) << 8) |
                       ((source[6] & (1 << 2)) << 7) |
                       ((source[7] & (1 << 2)) << 6) |
                       ((source[8] & (1 << 2)) << 5) |
                       ((source[9] & (1 << 2)) << 4) |
                       ((source[10] & (1 << 2)) << 3) |
                       ((source[11] & (1 << 2)) << 2) |
                       ((source[12] & (1 << 2)) << 1) |
                       ((source[13] & (1 << 2)) >> 0) |
                       ((source[14] & (1 << 2)) >> 1) |
                       ((source[15] & (1 << 2)) >> 2));

    destination[1] = (((source[0] & (1 << 1)) << 14) |
                       ((source[1] & (1 << 1)) << 13) |
                       ((source[2] & (1 << 1)) << 12) |
                       ((source[3] & (1 << 1)) << 11) |
                       ((source[4] & (1 << 1)) << 10) |
                       ((source[5] & (1 << 1)) << 9) |
                       ((source[6] & (1 << 1)) << 8) |
                       ((source[7] & (1 << 1)) << 7) |
                       ((source[8] & (1 << 1)) << 6) |
                       ((source[9] & (1 << 1)) << 5) |
                       ((source[10] & (1 << 1)) << 4) |
                       ((source[11] & (1 << 1)) << 3) |
                       ((source[12] & (1 << 1)) << 2) |
                       ((source[13] & (1 << 1)) << 1) |
                       ((source[14] & (1 << 1)) >> 0) |
                       ((source[15] & (1 << 1)) >> 1));

    destination[0] = (((source[0] & (1 << 0)) << 15) |
                       ((source[1] & (1 << 0)) << 14) |
                       ((source[2] & (1 << 0)) << 13) |
                       ((source[3] & (1 << 0)) << 12) |
                       ((source[4] & (1 << 0)) << 11) |
                       ((source[5] & (1 << 0)) << 10) |
                       ((source[6] & (1 << 0)) << 9) |
                       ((source[7] & (1 << 0)) << 8) |
                       ((source[8] & (1 << 0)) << 7) |
                       ((source[9] & (1 << 0)) << 6) |
                       ((source[10] & (1 << 0)) << 5) |
                       ((source[11] & (1 << 0)) << 4) |
                       ((source[12] & (1 << 0)) << 3) |
                       ((source[13] & (1 << 0)) << 2) |
                       ((source[14] & (1 << 0)) << 1) |
                       ((source[15] & (1 << 0)) >> 0));
}

void WINAPI TransposeBits_16xI8_to_8xI16(BYTE *pbSource, DWORD count)
{
    BYTE a[8], b[8];
    WORD tmp_dest[8];

    for (DWORD j = 0; j < count; j++)
    {
        TransposeByte8x8(pbSource + 0, a);
        TransposeByte8x8(pbSource + 8, b);

        for (char i = 0; i < 8; i++)
        {
            tmp_dest[i] = (a[i] << 8) | (b[i] << 0);
        }

        for (char i = 0; i < 16; i++)
        {
            pbSource[i] = ((BYTE *)tmp_dest)[i];
        }

        pbSource += 16;
    }
}

// a0,a1,..,a13; b0,b1,..,b13; ..;z0,z1,..z13
// a0,b0,..,z0; a1,b1,..,z1; ..; a13,b13,..,z13
void WINAPI Deinterleve_14x8Words_to_8x14Words(WORD *pwSource, DWORD count)
{
    WORD tmp[8][14];

    for (DWORD c = 0; c < count; c++)
    {
        for (DWORD i = 0; i < 8; i++)
        {
            for (DWORD j = 0; j < 14; j++)
            {
                tmp[i][j] = pwSource[(j * 8) + i];
            }
        }

        for (DWORD i = 0; i < 8 * 14; i++)
        {
            pwSource[i] = ((WORD *)tmp)[i];
        }
        pwSource += 14 * 8;
    }
}

void WINAPI TransposeBits_14xI16_to_16xI16(WORD *source, WORD *destination, DWORD chunks)
{
    WORD row;

    for (DWORD chunk_ctr = 0; chunk_ctr < chunks; chunk_ctr++)
    {
        for (BYTE i = 0; i < 16; i++)
        {
            destination[i] = 0;
        }

        for (BYTE row_ix = 0; row_ix < 14; row_ix++)
        {
            row = source[row_ix];
            for (BYTE col_ix = 0; col_ix < 16; col_ix++)
            {
                destination[col_ix] <<= 1;
                destination[col_ix] |= row & 0x0001;
                row >>= 1;
            }
        }
        source += 14;
        destination += 16;
    }
}

BYTE_TRANSPOSE_API  void WINAPI GenerateRandomBytestream(BYTE* destination, DWORD size, DWORD random_seed) {
    
    srand(random_seed);

    for (long int byte_ctr = 0; byte_ctr < size; byte_ctr++) {
        destination[byte_ctr] = rand();
    }
}

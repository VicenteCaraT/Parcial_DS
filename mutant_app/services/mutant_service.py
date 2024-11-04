import multiprocessing

class MutantService:
    
    @staticmethod
    def has_sequence(sequence):
        count = 1
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i - 1]:
                count += 1
                if count == 4:
                    return True
            else:
                count = 1
        return False

    @staticmethod
    def check_horizontal(row):
        return MutantService.has_sequence(row)

    @staticmethod
    def check_vertical(args):
        dna, col = args
        column = ''.join(dna[row][col] for row in range(len(dna)))
        return MutantService.has_sequence(column)

    @staticmethod
    def check_diagonal(args):
        dna, direction = args
        n = len(dna)
        
        if direction == 0:  # Diagonal de izquierda a derecha
            for start in range(n):
                diag_lr = ''.join(dna[i][start + i] for i in range(n) if start + i < n)
                if len(diag_lr) >= 4 and MutantService.has_sequence(diag_lr):
                    return True

            for start in range(1, n):
                diag_lr = ''.join(dna[start + i][i] for i in range(n) if start + i < n)
                if len(diag_lr) >= 4 and MutantService.has_sequence(diag_lr):
                    return True

        elif direction == 1:  # Diagonal de derecha a izquierda
            for start in range(n):
                diag_rl = ''.join(dna[i][n - 1 - start - i] for i in range(n) if n - 1 - start - i >= 0)
                if len(diag_rl) >= 4 and MutantService.has_sequence(diag_rl):
                    return True

            for start in range(1, n):
                diag_rl = ''.join(dna[start + i][n - 1 - i] for i in range(n) if start + i < n)
                if len(diag_rl) >= 4 and MutantService.has_sequence(diag_rl):
                    return True

        return False

    @staticmethod
    def is_mutant(dna):
        allowed_chars = {'A', 'T', 'C', 'G'}
        n = len(dna)

        # Validar estructura y caracteres del ADN
        for row in dna:
            if len(row) != n or any(char not in allowed_chars for char in row):
                return False

        sequence_count = 0

        # Pool de procesos para verificar cada dirección
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            horizontal_results = pool.map(MutantService.check_horizontal, dna)
            sequence_count += sum(horizontal_results)
            if sequence_count >= 2:
                return True

            vertical_results = pool.map(MutantService.check_vertical, [(dna, col) for col in range(n)])
            sequence_count += sum(vertical_results)
            if sequence_count >= 2:
                return True

            diagonal_results = pool.map(MutantService.check_diagonal, [(dna, direction) for direction in range(2)])
            sequence_count += sum(diagonal_results)
        
        return sequence_count > 1
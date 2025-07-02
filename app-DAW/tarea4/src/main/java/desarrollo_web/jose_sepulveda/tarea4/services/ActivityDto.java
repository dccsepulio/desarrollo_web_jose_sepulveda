package desarrollo_web.jose_sepulveda.tarea4.services;

import java.time.LocalDate;

public record ActivityDto(
    Long id,
    LocalDate fechaInicio,
    String sector,
    String nombre,
    String tema,
    Double notaPromedio
) {}


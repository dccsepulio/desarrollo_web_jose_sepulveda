/* 1 · Desactivar comprobación de claves foráneas solo mientras dura la migración */
SET FOREIGN_KEY_CHECKS = 0;

/* 2 · Eliminar constraints que referencian actividad.id */
ALTER TABLE nota   DROP FOREIGN KEY fk_nota_actividad1;
ALTER TABLE foto   DROP FOREIGN KEY fk_foto_actividad1;
ALTER TABLE contactar_por   DROP FOREIGN KEY fk_contactar_por_actividad1;
ALTER TABLE comentario   DROP FOREIGN KEY fk_comentario_actividad1;
ALTER TABLE actividad_tema   DROP FOREIGN KEY fk_actividad_tema_actividad1;
SELECT constraint_name, table_name
FROM information_schema.KEY_COLUMN_USAGE
WHERE referenced_table_name = 'actividad'
  AND referenced_column_name = 'id'
  AND constraint_schema = DATABASE();

/* 3 · Cambiar tipo en todas las columnas implicadas */
ALTER TABLE actividad
    MODIFY id BIGINT NOT NULL AUTO_INCREMENT;

ALTER TABLE nota
    MODIFY id BIGINT NOT NULL AUTO_INCREMENT,
    MODIFY actividad_id BIGINT NOT NULL;

/* si tuvieras foto u otras tablas que referencian actividad */
ALTER TABLE foto
    MODIFY id BIGINT NOT NULL AUTO_INCREMENT,
    MODIFY actividad_id BIGINT NOT NULL;

/* 4 · Volver a crear las claves foráneas */
ALTER TABLE nota
    ADD CONSTRAINT fk_nota_actividad1
        FOREIGN KEY (actividad_id)
        REFERENCES actividad(id)
        ON DELETE CASCADE;

ALTER TABLE foto
    ADD CONSTRAINT fk_foto_actividad1
        FOREIGN KEY (actividad_id)
        REFERENCES actividad(id)
        ON DELETE CASCADE;

ALTER TABLE contactar_por
    ADD CONSTRAINT fk_contactar_por_actividad1
        FOREIGN KEY (actividad_id)
        REFERENCES actividad(id)
        ON DELETE CASCADE;
ALTER TABLE comentario
    ADD CONSTRAINT fk_comentario_actividad1
        FOREIGN KEY (actividad_id)
        REFERENCES actividad(id)
        ON DELETE CASCADE;
ALTER TABLE actividad_tema
    ADD CONSTRAINT fk_actividad_tema_actividad1
        FOREIGN KEY (actividad_id)
        REFERENCES actividad(id)
        ON DELETE CASCADE;

/* 5 · Reactiva la comprobación de FK */
SET FOREIGN_KEY_CHECKS = 1;
